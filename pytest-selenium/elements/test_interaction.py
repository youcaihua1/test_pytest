"""
模块名称: test_interaction.py

功能描述:
    该模块的目标：展示了Selenium处理网页表单的基本操作，包括复选框状态切换和输入框内容管理
    
主要函数:
    
    
使用示例:
    >>> pytest -n 1 test_interaction.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

import pytest


def test_interactions():
    # 初始化WebDriver（创建Chrome浏览器实例）
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)  # 设置隐式等待时间为0.5秒（全局等待元素出现的时间）

    # 导航到测试页面
    driver.get("https://www.selenium.dev/selenium/web/inputs.html")

    # 定位并点击复选框元素
    check_input = driver.find_element(By.NAME, "checkbox_input")
    check_input.click()

    is_checked = check_input.is_selected()  # 获取复选框的选中状态
    assert is_checked == False  # 验证复选框是否未被选中

    # 定位并处理邮箱输入框
    email_input = driver.find_element(By.NAME, "email_input")
    email_input.clear()  # 清空输入框内容

    email = "admin@localhost.dev"
    email_input.send_keys(email)  # 在输入框中输入邮箱地址

    # 获取输入框的值
    data = email_input.get_attribute("value")
    assert data == email

    # 再次清空邮箱输入框
    email_input.clear()
    data = email_input.get_attribute("value")
    assert data == ""

    # 关闭浏览器并退出驱动
    driver.quit()
