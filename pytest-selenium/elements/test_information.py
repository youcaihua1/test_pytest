"""
模块名称: test_information.py

功能描述:
    该模块的目标：学习和应用 网页元素的各种属性和状态
    
    1、 元素状态检测方法

    =============================================
    方法               返回值      说明
    ------------------ ---------- ------------------------------------------
    is_displayed()     Boolean    元素是否可见（CSS display 不为 none）
    is_enabled()       Boolean    元素是否可用（未被 disabled）
    is_selected()      Boolean    复选框/单选按钮是否被选中
    =============================================

    2、 元素属性获取方法

    ============================================================================
    属性/方法                         返回值      说明
    --------------------------------- ---------- --------------------------------------
    tag_name                          String     HTML 标签名（小写）
    rect                              Dict       包含 x, y 坐标和 width, height 尺寸
    text                              String     元素的可见文本（包括子元素）
    get_attribute(name)               String     获取元素属性值
    value_of_css_property(prop)      String     获取计算后的 CSS 属性值
    ============================================================================


使用示例:
    >>> pytest -n 0 test_information.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
from selenium.webdriver.common.by import By

import pytest


def test_informarion(driver):
    driver.implicitly_wait(0.5)

    driver.get("https://www.selenium.dev/selenium/web/inputs.html")

    # 检查元素是否可见（is_displayed）
    is_email_visible = driver.find_element(By.NAME, "email_input").is_displayed()
    assert is_email_visible == True

    # 检查元素是否可用（is_enabled）
    is_enabled_button = driver.find_element(By.NAME, "button_input").is_enabled()
    assert is_enabled_button == True

    # 检查元素是否被选中（is_selected）
    is_selected_check = driver.find_element(By.NAME, "checkbox_input").is_selected()
    assert is_selected_check == True

    # 获取元素的标签名（tag_name）
    tag_name_inp = driver.find_element(By.NAME, "email_input").tag_name
    assert tag_name_inp == "input"

    # 获取元素的位置和尺寸信息（rect）
    rect = driver.find_element(By.NAME, "range_input").rect
    assert rect["x"] == 10

    # 获取元素的CSS属性值（value_of_css_property）
    css_value = driver.find_element(By.NAME, "color_input").value_of_css_property(
        "font-size"
    )
    assert css_value == "13.3333px"

    # 获取元素的文本内容（text）
    text = driver.find_element(By.TAG_NAME, "h1").text
    assert text == "Testing Inputs"

    # 获取元素的属性值（get_attribute）
    email_txt = driver.find_element(By.NAME, "email_input")
    value_info = email_txt.get_attribute("value")
    assert value_info == "admin@localhost"
