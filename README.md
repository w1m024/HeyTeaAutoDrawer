# HeyTeaAutoDrawer 🖌️

一个用于自动绘画的 Python 脚本，通过模拟鼠标操作，可在特定应用程序（如喜茶小程序）中自动绘制图像。

本项目**仅限 Windows 平台**运行。

这是因为项目的核心依赖 `pydirectinput` 是一个 Windows 独占库，它使用 DirectInput API 来模拟硬件级鼠标事件，以绕过某些应用程序的检测。

---

## 安装指南

建议使用 Conda 创建独立的 Python 虚拟环境。

```bash
# 1. 克隆本项目
git clone https://github.com/w1m024/HeyTeaAutoDrawer.git
cd HeyTeaAutoDrawer

# 2. 创建一个新的 conda 环境
conda create -n HeyTea python=3.10 -y

# 3. 激活环境
conda activate HeyTea

# 4. 安装所有依赖项
pip install -r requirements.txt
```

## 使用说明

本项目同时支持命令行（CLI）和图形界面（GUI）两种使用方式：

### CLI

1. 在项目根目录创建 `images/` 并放入参考图片（例如 `cat.png`）。
2. 在终端中运行：
```powershell
python main.py cat.png
```

### GUI
1. 启动 GUI：
```powershell
python gui.py
```
2. 简要说明：
- 菜单 -> 文件 -> 打开文件：选择图片并预览；
- 菜单 -> 设置 -> 修改当前配置：可在窗口内编辑配置并保存；
- 菜单 -> 设置 -> 选择画板范围：交互式框选屏幕区域以更新 `screen_config`；
