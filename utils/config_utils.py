# utils/config_utils.py
# -*- coding: utf-8 -*-
"""
配置文件管理模块
负责：读取、保存、显示、修改 config/config.py
"""
import os
import pprint
import importlib.util
from utils.config_help import CONFIG_HELP
from utils.print_utils import print_title, print_info, print_success, print_section, print_error, print_step


def load_config(path="config/config.py"):
    """动态加载配置文件"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到配置文件: {path}")
    spec = importlib.util.spec_from_file_location("config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CONFIG


def save_config(config, path="config/config.py"):
    """保存配置文件到本地"""
    with open(path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\nCONFIG = ")
        pprint.pprint(config, stream=f, width=100, compact=False)
    print_success("配置文件已保存")


def show_config(config):
    """打印当前配置及说明"""
    print_title("当前配置")
    for section, params in config.items():
        print(f"\n[{section}]")
        for k, v in params.items():
            desc = CONFIG_HELP.get(section, {}).get(k, "（无说明）")
            print(f"  {k:<18} = {v:<10}  # {desc}")
    print("=" * 60)


def modify_config(config, key_path, value, path="config/config.py"):
    """
    修改配置，例如:
    modify_config(CONFIG, "image_config.W_IMG", "1024")
    """
    try:
        section, key = key_path.split(".", 1)
        if section not in config or key not in config[section]:
            raise KeyError
        old_val = config[section][key]

        # 自动类型推断
        try:
            value = eval(value)
        except Exception:
            pass

        config[section][key] = value
        print_success(f"{section}.{key}: {old_val} → {value}")
        save_config(config, path)
    except Exception:
        print_error(f"无效参数: {key_path}")
        print_step("示例: python main.py --set image_config.W_IMG=1024")
