# utils/print_utils.py
# -*- coding: utf-8 -*-
"""
统一打印输出工具模块
提供一致的打印风格和引导词
"""


def print_title(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_info(text):
    """打印信息"""
    print(f"ℹ️  {text}")


def print_success(text):
    """打印成功信息"""
    print(f"✅ {text}")


def print_warning(text):
    """打印警告信息"""
    print(f"⚠️  {text}")


def print_error(text):
    """打印错误信息"""
    print(f"❌ {text}")


def print_step(text):
    """打印步骤信息"""
    print(f"→ {text}")


def print_progress(current, total, text=""):
    """打印进度信息"""
    if text:
        print(f"进度: {current}/{total} {text}")
    else:
        print(f"进度: {current}/{total}")


def print_section(text):
    """打印分割线"""
    print("-" * 60)
    print(text)


def print_countdown(seconds):
    """打印倒计时"""
    for i in range(seconds, 0, -1):
        print(f"  {i}...", end="\r")
        import time
        time.sleep(1)
    print("  开始！  ")
