# utils/drawing_utils.py
# -*- coding: utf-8 -*-

import time

# 仅使用 pydirectinput 库来模拟鼠标操作
import pydirectinput
import pydirectinput as mouse_ctrl
from utils.print_utils import print_error, print_warning

def to_screen_coord(x_img, y_img, image_cfg, screen_cfg):
    """
    将图像坐标 (x_img, y_img) 映射到屏幕坐标。
    """
    try:
        W_IMG = int(image_cfg["W_IMG"])
        H_IMG = int(image_cfg["H_IMG"])
    except Exception as e:
        raise KeyError(f"image_config 缺少 W_IMG/H_IMG: {e}")

    try:
        X_A = int(screen_cfg["X_A"])
        Y_A = int(screen_cfg["Y_A"])
        W = float(screen_cfg["W"])
        H = float(screen_cfg["H"])
    except Exception as e:
        raise KeyError(f"screen_config 缺少 X_A/Y_A/W/H: {e}")


    # 计算映射（保持浮点精度再转 int）
    x_screen = X_A + (x_img / W_IMG) * W
    y_screen = Y_A + (y_img / H_IMG) * H
    return int(round(x_screen)), int(round(y_screen))
def execute_drawing(path, config=None):
    press_delay = 0.001
    if isinstance(config, dict):
        press_delay = float(config.get("draw_config", {}).get("PRESS_DELAY", press_delay))

    if pydirectinput is None:
        raise RuntimeError("execute_drawing: 无法找到 pydirectinput 库")

    try:
        assert isinstance(path, list) and len(path) >= 2 and \
               all(isinstance(i, tuple) and len(i) == 2 for i in path), \
               f"输入参数无效，path 必须是 [(x1, y1), (x2, y2), ...] 格式，但收到 {path}"
        
        x_start, y_start = path[0]
        pydirectinput.moveTo(int(x_start), int(y_start))
        
        pydirectinput.mouseDown()
        
        for (x, y) in path[1:]:
            pydirectinput.moveTo(int(x), int(y))


        time.sleep(press_delay)
        pydirectinput.mouseUp()
        time.sleep(press_delay)

    except pydirectinput.FailSafeException:
        print_warning("中止：绘图操作被中断（鼠标移至屏幕角落）")
        raise
    except Exception as e:
        print_error(f"绘制过程出错: {e}")
        raise
