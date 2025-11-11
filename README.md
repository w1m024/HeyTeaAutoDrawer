# HeyTeaAutoDrawer 🖌️

一个用于自动绘画的 Python 脚本，通过模拟鼠标操作，可在特定应用程序（如喜茶小程序）中自动绘制图像。

本项目**仅限 Windows 平台**运行。

这是因为项目的核心依赖 `pydirectinput` 是一个 Windows 独占库，它使用 DirectInput API 来模拟硬件级鼠标事件，以绕过某些应用程序的检测。

---

## 安装指南

建议使用 Conda 创建独立的 Python 虚拟环境。

```bash
# 1. 克隆本项目
git clone https://github.com/username/HeyTeaAutoDrawer.git
cd HeyTeaAutoDrawer

# 2. 创建一个新的 conda 环境
conda create -n HeyTea python=3.10 -y

# 3. 激活环境
conda activate HeyTea

# 4. 安装所有依赖项
pip install -r requirements.txt
```

## 使用说明

1. 新建文件夹 `images/`，将参考图(如cat.png)粘贴到 `images/` 文件夹中
2. 在命令行中运行
```bash
python main.py cat.png
```
3. 根据提示信息继续操作
