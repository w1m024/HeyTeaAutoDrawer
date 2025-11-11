# main.py
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from InquirerPy import inquirer

from utils.coord_utils import capture_screen_region
from utils.image_utils import auto_fill_image_config
from utils.config_utils import load_config, save_config, show_config, modify_config
from utils.print_utils import print_info, print_success, print_warning, print_error, print_step, print_section, print_countdown
from core.auto_drawer_canny import AutoDrawerCanny
from core.auto_drawer_scan import AutoDrawerScan
from utils.config_help import CONFIG_HELP


def tui_modify_config(config):
    while True:
        sections = list(config.keys()) + ["返回主菜单"]
        section = inquirer.select(
            message="选择配置类别：",
            choices=sections,
        ).execute()

        if section == "返回主菜单":
            save_config(config)
            break

        params = config[section]
        choices = [f"{key} = {val}" for key, val in params.items()] + ["返回上一级"]
        choice = inquirer.select(
            message=f"选择要修改的参数（{section}）：",
            choices=choices,
        ).execute()

        if choice == "返回上一级":
            continue

        key = choice.split("=")[0].strip()
        desc = CONFIG_HELP.get(section, {}).get(key, "无说明")
        print(f"\n当前值：{params[key]} ({desc})")

        new_value = inquirer.text(
            message="请输入新值（回车取消）:",
            default=str(params[key]),
        ).execute()

        if not new_value.strip():
            print_warning("未修改该项")
            continue

        try:
            try:
                new_value_eval = eval(new_value)
            except Exception:
                new_value_eval = new_value

            old_value = params[key]
            config[section][key] = new_value_eval
            print_success(f"{section}.{key}: {old_value} → {new_value_eval}")
            save_config(config)
        except Exception as e:
            print_error(f"修改失败: {e}")
        print_section("")


def tui_draw_menu(config, image_path):
    """绘画二级菜单"""
    drawer_canny = AutoDrawerCanny(config)
    drawer_scan = AutoDrawerScan(config)

    while True:
        draw_choice = inquirer.select(
            message="选择绘画方式：",
            choices=[
                "Canny 边缘绘画",
                "预览 Canny 边缘",
                "Scan 扫描线绘画",
                "返回主菜单"
            ],
        ).execute()

        if draw_choice == "返回主菜单":
            break
        elif draw_choice.startswith("预览"):
            drawer_canny.preview(image_path)
        elif draw_choice.startswith("Canny"):
            drawer_canny.run(image_path)
        elif draw_choice.startswith("Scan"):
            drawer_scan.run(image_path)


def main():
    parser = argparse.ArgumentParser(description="自动绘图系统")
    parser.add_argument("image", nargs="?", help="图片文件名（位于 images/ 文件夹下）")
    parser.add_argument("--show-config", action="store_true", help="查看当前配置")
    parser.add_argument("--set", type=str, help="修改配置，例如 image_config.W_IMG=1024")
    args = parser.parse_args()

    config = load_config()

    if args.show_config:
        show_config(config)
        return

    if args.set:
        key, value = args.set.split("=", 1)
        modify_config(config, key.strip(), value.strip())
        return

    if not args.image:
        print_info("使用示例：")
        print("  python main.py cat.jpg")
        print("  python main.py --show-config")
        print("  python main.py --set draw_config.DELAY=5")
        return

    image_name = args.image
    image_path = os.path.join("images", image_name)
    if not os.path.exists(image_path):
        print_error(f"图片不存在: {image_path}")
        return

    if config["screen_config"]["W"] <= 0:
        print_step("启动捕获工具...")
        X_A, Y_A, W, H = capture_screen_region("config/config.py")
        config["screen_config"].update({"X_A": X_A, "Y_A": Y_A, "W": W, "H": H})
        save_config(config)

    config = auto_fill_image_config(config, image_path)
    save_config(config)

    while True:
        main_choice = inquirer.select(
            message="请选择操作：",
            choices=[
                "修改配置",
                "查看当前配置",
                "重选画板范围",
                "开始绘画",
                "退出"
            ],
        ).execute()

        if main_choice == "修改配置":
            tui_modify_config(config)

        elif main_choice == "绘画":
            tui_draw_menu(config, image_path)

        elif main_choice == "查看当前配置":
            show_config(config)

        elif main_choice == "重选画板范围":
            print_step("请框选新的画板区域...")
            X_A, Y_A, W, H = capture_screen_region("config/config.py")
            config["screen_config"].update({"X_A": X_A, "Y_A": Y_A, "W": W, "H": H})
            save_config(config)
            print_success(f"画板坐标已更新: ({X_A}, {Y_A}), 尺寸 {W}×{H}")

        elif main_choice == "退出":
            print_info("程序已退出")
            break



if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    main()
