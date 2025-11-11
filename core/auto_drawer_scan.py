# core/auto_drawer_scan.py
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from tqdm import tqdm
from utils.drawing_utils import to_screen_coord, execute_drawing
from utils.print_utils import print_info, print_success, print_step, print_countdown


class AutoDrawerScan:
    """
    垂直扫描线绘图算法
    逐列扫描图像亮度，检测变化区域并在屏幕上绘制线条。
    """

    def __init__(self, config):
        self.config = config
        self.image_config = config["image_config"]
        self.draw_config = config["draw_config"]
        self.screen_config = config["screen_config"]

    def run(self, image_path):
        print_step("加载图像...")
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h, w = gray.shape
        brush_step = self.image_config.get("BRUSH_STEP", 3)
        threshold = self.image_config.get("THRESHOLD_VALUE", 128)
        delay = self.draw_config.get("DELAY", 3)
        speed_factor = self.draw_config.get("SPEED_FACTOR", 1.0)

        print_countdown(delay)
        print_step("开始绘制...")
        start_time = time.time()

        # 按列扫描
        for col in tqdm(range(0, w, brush_step), desc="绘制中", unit="列"):
            line = gray[:, col]  # 取该列所有像素（垂直方向）
            y_coords = np.where(line < threshold)[0]
            if len(y_coords) == 0:
                continue

            # 将连续的黑色像素区域视为一条竖线段
            start_y = y_coords[0]
            for i in range(1, len(y_coords)):
                if y_coords[i] - y_coords[i - 1] > 2:
                    end_y = y_coords[i - 1]
                    self._draw_column_segment(col, start_y, end_y)
                    start_y = y_coords[i]
            # 绘制最后一段
            self._draw_column_segment(col, start_y, y_coords[-1])

            time.sleep(0.001 / speed_factor)  # 控制绘制速度

        elapsed = time.time() - start_time
        print_success(f"绘制完成！总用时 {elapsed:.2f} 秒")

    def _draw_column_segment(self, x, y1, y2):
        """在屏幕上绘制一条竖直线段"""
        x_screen, y1_screen = to_screen_coord(x, y1, self.image_config, self.screen_config)
        _, y2_screen = to_screen_coord(x, y2, self.image_config, self.screen_config)

        path = [(x_screen, y1_screen), (x_screen, y2_screen)]
        execute_drawing(path, self.config)
