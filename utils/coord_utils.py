# utils/coord_utils.py
# -*- coding: utf-8 -*-
"""
coord_utils.py - 屏幕画板区域捕获工具
"""
import time
import importlib.util
import os
import pprint
from pynput import mouse
from utils.print_utils import print_title, print_info, print_success, print_step, print_section


def capture_screen_region(config_path="config/config.py"):
    """捕获画板区域坐标并写入配置文件。"""
    print_title("画板区域捕获工具")
    print_info("请准备好画板窗口，3 秒后开始监听...")
    time.sleep(3)

    start, end = None, None

    print_step("请按下左键，从画板【左上角】拖到【右下角】，然后松开")

    def on_click(x, y, button, pressed):
        nonlocal start, end
        if button == mouse.Button.left:
            if pressed:
                start = (int(x), int(y))
                print_info(f"已记录左上角: ({x}, {y})")
            else:
                end = (int(x), int(y))
                print_info(f"已记录右下角: ({x}, {y})")
                return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if not start or not end:
        raise RuntimeError("未捕获有效坐标，请重试")

    X_A, Y_A = start
    X_B, Y_B = end
    W, H = abs(X_B - X_A), abs(Y_B - Y_A)
    if X_A > X_B:
        X_A = X_B
    if Y_A > Y_B:
        Y_A = Y_B

    print_success(f"捕获成功！左上角({X_A},{Y_A}) 尺寸 {W}×{H}")
    _update_config(config_path, X_A, Y_A, W, H)
    return X_A, Y_A, W, H


def _update_config(config_path, X_A, Y_A, W, H):
    """更新 config/config.py"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(config_path)

    spec = importlib.util.spec_from_file_location("config", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = module.CONFIG
    config["screen_config"].update({"X_A": X_A, "Y_A": Y_A, "W": W, "H": H})

    with open(config_path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# 自动更新的配置文件，请勿手动修改 screen_config。\n\n")
        f.write("CONFIG = ")
        pprint.pprint(config, stream=f, width=100, compact=False)
    print_success("config/config.py 已保存")
