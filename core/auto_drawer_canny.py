# core/auto_drawer_canny.py
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from tqdm import tqdm
from utils.drawing_utils import to_screen_coord, execute_drawing
from utils.print_utils import print_info, print_success, print_error, print_step, print_countdown


class AutoDrawerCanny:
    """Canny 边缘绘图算法类"""

    def __init__(self, config):
        self.config = config
        self.img_cfg = config["image_config"]
        self.draw_cfg = config["draw_config"]
        self.screen_cfg = config["screen_config"]

    def generate_paths_from_image(self, image_path):
        """生成绘图路径"""
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(image_path)

        W, H = self.img_cfg["W_IMG"], self.img_cfg["H_IMG"]
        img = cv2.resize(img, (W, H))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(
            blur,
            self.img_cfg.get("CANNY_THRESH1", 50),
            self.img_cfg.get("CANNY_THRESH2", 150)
        )

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        paths = []
        for cnt in contours:
            if cv2.arcLength(cnt, True) < 10:
                continue
            eps = self.img_cfg.get("EPSILON_FACTOR", 0.001) * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, eps, True)
            path = [(int(x), int(y)) for [[x, y]] in approx]
            paths.append(path)

        print_info(f"提取 {len(paths)} 条路径")
        return paths

    def preview(self, image_path):
        """显示 Canny 边缘预览窗口"""
        print_step("生成 Canny 边缘预览...")
        img = cv2.imread(image_path)
        if img is None:
            print_error(f"无法读取图片: {image_path}")
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(
            gray,
            self.img_cfg["CANNY_THRESH1"],
            self.img_cfg["CANNY_THRESH2"]
        )

        preview_img = cv2.bitwise_not(edges)

        # preview_img = cv2.bitwise_and(img, img, mask=edges)
        
        
        board_w = self.screen_cfg.get("W", 800)
        board_h = self.screen_cfg.get("H", 600)
        cv2.namedWindow("Canny 预览", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Canny 预览", board_w, board_h)
        
        cv2.imshow("Canny 预览", preview_img)
        print_info("按任意键关闭预览窗口")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self, image_path):
        """执行完整绘制流程"""
        paths = self.generate_paths_from_image(image_path)
        brush_step = self.img_cfg.get("BRUSH_STEP", 3)
        delay = self.draw_cfg.get("DELAY", 3)
        speed_factor = self.draw_cfg.get("SPEED_FACTOR", 1.0)

        print_countdown(delay)
        print_step("开始绘制...")
        start_time = time.time()
        
        # 遍历 Canny 提取的每一条轮廓 (path)
        for path in tqdm(paths, desc="绘制中", unit="路径"):
            sampled_path_img = path[::brush_step]

            if len(sampled_path_img) < 2:
                continue
              
            full_screen_path = []
            
            for (x_img, y_img) in sampled_path_img:
                x_screen, y_screen = to_screen_coord(x_img, y_img, self.img_cfg, self.screen_cfg)
                full_screen_path.append((x_screen, y_screen))

            if len(full_screen_path) >= 2:
                execute_drawing(full_screen_path, self.config)
            
        elapsed = time.time() - start_time
        print_success(f"绘制完成！总用时 {elapsed:.2f} 秒")
