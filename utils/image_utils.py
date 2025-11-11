# utils/image_utils.py
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from utils.print_utils import print_info


def auto_fill_image_config(config, image_path, max_size=1280):
    """
    自动根据图片更新 image_config 参数：
    - 自动计算图像缩放尺寸
    - 使用 OTSU 自动估计阈值
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    h, w = img.shape[:2]
    scale = min(max_size / max(w, h), 1.0)
    W_IMG, H_IMG = int(w * scale), int(h * scale)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 正确写法：获取 Otsu 自动阈值
    threshold_val, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    threshold = int(threshold_val)

    config["image_config"]["W_IMG"] = W_IMG
    config["image_config"]["H_IMG"] = H_IMG
    config["image_config"]["THRESHOLD_VALUE"] = threshold

    print_info(f"自动配置: W_IMG={W_IMG}, H_IMG={H_IMG}, THRESHOLD={threshold}")
    return config
