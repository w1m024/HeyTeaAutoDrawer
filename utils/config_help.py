# utils/config_help.py
# -*- coding: utf-8 -*-
"""
配置参数说明，用于命令行帮助和交互修改。
"""

CONFIG_HELP = {
    "screen_config": {
        "X_A": "画板左上角 X 坐标（屏幕像素）",
        "Y_A": "画板左上角 Y 坐标（屏幕像素）",
        "W": "画板宽度（像素）",
        "H": "画板高度（像素）",
    },
    "image_config": {
        "W_IMG": "绘图图像缩放后的宽度",
        "H_IMG": "绘图图像缩放后的高度",
        "THRESHOLD_VALUE": "二值化阈值（用于扫描线法）",
        "BRUSH_STEP": "笔刷间隔（像素）",
        "CANNY_THRESH1": "Canny 边缘检测阈值下限",
        "CANNY_THRESH2": "Canny 边缘检测阈值上限",
        "EPSILON_FACTOR": "边缘轮廓简化精度（越小越精细）",
    },
    "draw_config": {
        "DELAY": "绘制前倒计时（秒）",
        "ENABLE_JITTER": "是否启用笔画抖动效果",
        "JITTER_AMOUNT": "抖动幅度（像素）",
        "JITTER_FREQUENCY": "抖动频率（笔画间隔）",
    }
}
