"""
模块名称: test_navigation.py

功能描述:
    该模块的目标：学习浏览器的基本导航功能，包括页面加载、前进、后退和刷新操作
    
主要函数:
    driver.get("https://www.selenium.dev")  # 打开 Selenium 官方主页
    driver.back()  # 导航回上一个页面
    driver.forward()  # 导航到下一个页面
    driver.refresh()  # 刷新当前页面
    
使用示例:
    > pytest -n 0 test_navigation.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""


def test_navigation(driver):
    driver.get("https://www.selenium.dev")  # 导航到第一个网站：Selenium 官方主页
    driver.get("https://www.selenium.dev/selenium/web/index.html")  # 导航到第二个网站：Selenium WebDriver 测试页面索引

    title = driver.title
    assert title == "Index of Available Pages"

    driver.back()  # 执行后退操作（返回上一个页面）
    title = driver.title
    assert title == "Selenium"

    driver.forward()  # 执行前进操作（回到下一个页面）
    title = driver.title
    assert title == "Index of Available Pages"

    driver.refresh()  # 刷新当前页面
    title = driver.title
    assert title == "Index of Available Pages"
