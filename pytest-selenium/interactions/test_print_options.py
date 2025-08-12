"""
模块名称: test_print_options.py

功能描述:
    该模块的目标：展示了Selenium的打印功能配置选项
    
主要函数:
    
    
使用示例:
    > pytest -n 7 test_print_options.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import base64
import pytest

from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions


def test_orientation(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()  # 创建打印选项对象
    print_options.orientation = "landscape"  # 设置打印方向为横向（可选值："landscape" 或 "portrait"）
    assert print_options.orientation == "landscape"
    # 执行打印命令
    print_result = driver.print_page(print_options)

    # 保存为PDF
    with open("output.pdf", "wb") as f:
        f.write(base64.b64decode(print_result))


def test_range(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()
    print_options.page_ranges = ["1, 2, 3"]  # 设置打印页面范围（格式示例：["1,2,3"] 或 ["1-3"]）
    assert print_options.page_ranges == ["1, 2, 3"]


def test_size(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()
    print_options.page_height = 27.94      # 设置页面高度为27.94厘米（A4纸高度）  注意：page_width用于设置宽度
    assert print_options.page_height == 27.94


def test_margin(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()
    print_options.margin_top = 10  # 设置四个方向的页边距（单位：厘米）
    print_options.margin_bottom = 10
    print_options.margin_left = 10
    print_options.margin_right = 10
    assert print_options.margin_top == 10
    assert print_options.margin_bottom == 10
    assert print_options.margin_left == 10
    assert print_options.margin_right == 10


def test_scale(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()
    print_options.scale = 0.5  # 设置打印缩放比例为50%（范围：0.1 到 2.0）
    current_scale = print_options.scale
    assert current_scale == 0.5


def test_background(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()
    print_options.background = True  # 设置是否打印背景（True：打印背景，False：不打印背景）
    assert print_options.background is True


def test_shrink_to_fit(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()
    print_options.shrink_to_fit = True  # 设置是否自适应页面（True：缩放内容以适应页面，False：不缩放）
    assert print_options.shrink_to_fit is True
