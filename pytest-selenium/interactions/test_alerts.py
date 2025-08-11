"""
模块名称: test_alerts.py

功能描述:
    该模块的目标：展示了如何处理三种不同类型的浏览器弹窗
    
    Selenium 弹窗处理核心方法
    ================================================================
    方法                    功能                    适用弹窗类型
    ---------------------- ----------------------- -----------------
    `switch_to.alert`      切换到当前弹窗            所有类型
    `alert.text`           获取弹窗文本内容          所有类型
    `alert.accept()`       接受弹窗(确定/是)         所有类型
    `alert.dismiss()`      取消弹窗(取消/否)         确认弹窗
    `alert.send_keys()`    在输入框中输入文本        提示弹窗
    ================================================================
    
    
使用示例:
    >>> pytest -n 3 test_alerts.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

global url
url = "https://www.selenium.dev/documentation/webdriver/interactions/alerts/"


def test_alert_popup():
    driver = webdriver.Chrome()
    driver.get(url)
    # 定位并点击触发警告弹窗的链接
    element = driver.find_element(By.LINK_TEXT, "See an example alert")
    element.click()

    wait = WebDriverWait(driver, timeout=2)
    alert = wait.until(lambda d: d.switch_to.alert)  # 等待弹窗出现并切换到弹窗
    text = alert.text
    alert.accept()  # 接受弹窗（点击确定按钮）
    assert text == "Sample alert"
    driver.quit()


def test_confirm_popup(driver):
    driver.get(url)
    element = driver.find_element(By.LINK_TEXT, "See a sample confirm")  # 定位触发确认弹窗的链接
    driver.execute_script("arguments[0].click();", element)  # 使用JavaScript点击链接（避免可能的点击拦截问题）

    wait = WebDriverWait(driver, timeout=2)
    alert = wait.until(lambda d: d.switch_to.alert)
    text = alert.text
    alert.dismiss()  # 取消弹窗（点击取消按钮）
    assert text == "Are you sure?"


def test_prompt_popup(driver):
    driver.get(url)
    element = driver.find_element(By.LINK_TEXT, "See a sample prompt")  # 定位触发提示弹窗的链接
    driver.execute_script("arguments[0].click();", element)  # 使用JavaScript点击链接

    wait = WebDriverWait(driver, timeout=2)
    alert = wait.until(lambda d: d.switch_to.alert)
    alert.send_keys("Selenium")
    text = alert.text
    alert.accept()
    assert text == "What is your tool of choice?"
