(# xicha_drow

本仓库用于「再喜茶」小程序杯贴的自动绘制工具。下面是一个在 Windows（PowerShell）上使用虚拟环境创建、安装依赖并运行的简短快速指南。

## 快速开始 — 在 Windows PowerShell 下使用 venv

1. 创建虚拟环境（在项目根目录下）：

```powershell
python -m venv venv
```

2. 激活虚拟环境（PowerShell）：

```powershell
.\venv\Scripts\Activate.ps1
```

如果遇到“脚本被禁用”的错误，可以临时允许当前用户运行签名脚本：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# 然后重新运行 Activate.ps1
.\venv\Scripts\Activate.ps1
```

3. 升级 pip（可选）：

```powershell
python -m pip install -U pip
```

4. 安装依赖：

```powershell
pip install -r requirements.txt
```

5. 运行程序或查看帮助：

```powershell
python main.py --help
# 或直接运行主脚本
python main.py
```

6. 退出虚拟环境：

```powershell
deactivate
```

## 说明
- `requirements.txt` 位于仓库根目录，包含本项目在代码中用到的第三方包（如 numpy、opencv-python、tqdm、InquirerPy、pynput、pydirectinput）。
- `pydirectinput` 为 Windows 专用，运行时可能需要对窗口焦点与权限有额外注意（工具会模拟鼠标/键盘操作）。

如果你希望我把依赖固定为具体版本（便于可复现环境），我可以把常用稳定版本写入 `requirements.txt` 并提交。欢迎告诉我你的偏好。

