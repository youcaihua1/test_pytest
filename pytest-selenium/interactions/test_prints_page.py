"""
模块名称: test_prints_page.py

功能描述:
    该模块的目标：打印浏览器页面
    
主要函数:
    
    
使用示例:
    > pytest -n 0 test_prints_page.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions  # 导入PrintOptions类，用于配置页面打印选项


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_prints_page(driver):
    driver.get("https://www.selenium.dev/")
    print_options = PrintOptions()  # 创建打印选项对象

    # 调用WebDriver的print_page方法打印当前页面
    # 使用上面配置的打印选项
    # 方法返回PDF文件的base64编码字符串
    pdf = driver.print_page(print_options)
    assert len(pdf) > 0  # 断言：检查返回的PDF内容是否不为空
