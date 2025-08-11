"""
模块名称: test_interactions.py

功能描述:
    该模块的目标：简单的一个浏览器交互

    
使用示例:
    >>> pytest -n 0 test_interactions.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""


def test_interactions(driver):
    driver.get("https://www.selenium.dev")

    title = driver.title
    assert title == "Selenium"

    url = driver.current_url
    assert url == "https://www.selenium.dev/"
