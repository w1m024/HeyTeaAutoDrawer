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


def get_default_config():
    """Return the default CONFIG.

    By default this will attempt to load `config/config.default.py` (the
    dedicated defaults file). If that file can't be read for any reason,
    fall back to an inline default dict so callers remain resilient.
    """
    default_path = "config/config.default.py"
    try:
        # load_config dynamically loads the module and returns module.CONFIG
        return load_config(default_path)
    except Exception:
        # Fallback: same defaults that are expected to be in config.default.py
        return {
            'draw_config': {
                'DELAY': 3,
                'ENABLE_JITTER': True,
                'JITTER_AMOUNT': 1.5,
                'JITTER_FREQUENCY': 2,
                'SPEED_FACTOR': 1
            },
            'image_config': {
                'BRUSH_STEP': 3,
                'CANNY_THRESH1': 50,
                'CANNY_THRESH2': 150,
                'EPSILON_FACTOR': 0.0001,
                'H_IMG': 0,
                'THRESHOLD_VALUE': 0,
                'W_IMG': 0
            },
            'screen_config': {
                'H': 0,
                'W': 0,
                'X_A': 0,
                'Y_A': 0
            }
        }


def reset_config_preserve_special(config, path="config/config.py"):
    """
    Reset a config dict to the defaults defined in get_default_config(),
    but preserve these existing values from `config`:
      - image_config.H_IMG
      - image_config.W_IMG
      - image_config.THRESHOLD_VALUE
      - the entire screen_config dict

    The resulting config is saved to `path` via save_config().
    """
    try:
        defaults = get_default_config()

        # preserve image special values if they exist in current config
        img_cfg = config.get('image_config', {})
        preserve_H = img_cfg.get('H_IMG', defaults['image_config']['H_IMG'])
        preserve_W = img_cfg.get('W_IMG', defaults['image_config']['W_IMG'])
        preserve_thresh = img_cfg.get('THRESHOLD_VALUE', defaults['image_config']['THRESHOLD_VALUE'])

        # preserve screen_config entirely
        preserve_screen = config.get('screen_config', defaults['screen_config'])

        # start from defaults then re-apply preserved values
        new_config = defaults
        new_config['image_config']['H_IMG'] = preserve_H
        new_config['image_config']['W_IMG'] = preserve_W
        new_config['image_config']['THRESHOLD_VALUE'] = preserve_thresh
        new_config['screen_config'] = preserve_screen

        save_config(new_config, path)
        print_success("配置已重置为默认值（保留指定项）")
    except Exception as e:
        print_error(f"重置配置失败: {e}")


def reset_config_file(path="config/config.py"):
    """Load config from `path`, reset it preserving special keys, and save back."""
    try:
        cfg = load_config(path)
        reset_config_preserve_special(cfg, path)
    except FileNotFoundError:
        print_error(f"未找到配置文件: {path}")
    except Exception as e:
        print_error(f"重置配置时发生错误: {e}")
