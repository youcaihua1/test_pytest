"""
模块名称: using_selenium_tests.py

功能描述:
    该模块的目标：使用pytest和selenium来进行网页测试。测试是否成功提交表单。
    
主要函数:
    driver：测试夹具，为测试函数提供导航到目标页面的Chrome浏览器实例，并在测试后自动关闭。
    
使用示例:
    >>> pytest using_selenium_tests.py
    >>> pytest -n 0 using_selenium_tests.py (不使用并行执行)
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/8
修改历史:
    1. 2025/8/8 - 创建文件
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    service = Service(r'D:\Programs\driver\chromedriver-win64\chromedriver.exe')  # 手动指定 ChromeDriver 位置
    # 没有指定service时，运行该模块，有一个警告信息：
    # Selenium在使用Selenium Manager（Selenium 4的一个内置工具，用于自动管理浏览器驱动）时，
    # 尝试从指定的URL下载Chrome浏览器版本信息时发生了网络请求错误。虽然不影响运行结果，不过还是添加这个指定路径。
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    yield driver
    driver.quit()


def test_eight_components(driver):
    title = driver.title
    assert title == "Web form"

    driver.implicitly_wait(3)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()  # 点击按钮 提交表单
    # 提交表单后，页面将会跳转，测试页面是否跳转。
    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"
