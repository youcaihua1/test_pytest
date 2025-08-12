"""
模块名称: test_wheel.py

功能描述:
    该模块的目标：学习和使用 Selenium 的滚动功能
    
主要函数:
    直接滚动到元素 (scroll_to_element)
    按像素精确滚动 (scroll_by_amount)
    从元素/坐标点开始滚动 (scroll_from_origin)
    
使用示例:
    > pytest -n 5 test_wheel.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin  # 提供滚动操作控制


def test_can_scroll_to_element(driver):
    driver.get("https://selenium.dev/selenium/web/scrolling_tests/frame_with_nested_scrolling_frame_out_of_view.html")

    iframe = driver.find_element(By.TAG_NAME, "iframe")  # 定位目标iframe元素
    # 创建动作链：滚动到指定元素
    ActionChains(driver)\
        .scroll_to_element(iframe)\
        .perform()

    assert _in_viewport(driver, iframe)


def test_can_scroll_from_viewport_by_amount(driver):
    driver.get("https://selenium.dev/selenium/web/scrolling_tests/frame_with_nested_scrolling_frame_out_of_view.html")

    footer = driver.find_element(By.TAG_NAME, "footer")
    delta_y = footer.rect['y']  # 获取元素的Y坐标（距页面顶部距离）
    # 创建动作链：垂直滚动指定距离
    # 水平滚动0，垂直滚动delta_y像素
    ActionChains(driver)\
        .scroll_by_amount(0, delta_y)\
        .perform()

    sleep(0.5)
    assert _in_viewport(driver, footer)


def test_can_scroll_from_element_by_amount(driver):
    driver.get("https://selenium.dev/selenium/web/scrolling_tests/frame_with_nested_scrolling_frame_out_of_view.html")

    iframe = driver.find_element(By.TAG_NAME, "iframe")
    scroll_origin = ScrollOrigin.from_element(iframe)  # 创建以该元素为原点的滚动源
    # 创建动作链：从元素原点滚动200px
    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 200)\
        .perform()

    sleep(0.5)
    driver.switch_to.frame(iframe)  # 切换到iframe内部
    checkbox = driver.find_element(By.NAME, "scroll_checkbox")  # 定位iframe内的复选框
    assert _in_viewport(driver, checkbox)


def test_can_scroll_from_element_with_offset_by_amount(driver):
    driver.get("https://selenium.dev/selenium/web/scrolling_tests/frame_with_nested_scrolling_frame_out_of_view.html")

    footer = driver.find_element(By.TAG_NAME, "footer")
    scroll_origin = ScrollOrigin.from_element(footer, 0, -50)  # 创建带偏移的滚动源：Y轴向上偏移50px（负号表示向上）
    # 创建动作链：从偏移点滚动200px
    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 200)\
        .perform()

    sleep(0.5)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    checkbox = driver.find_element(By.NAME, "scroll_checkbox")
    assert _in_viewport(driver, checkbox)


def test_can_scroll_from_viewport_with_offset_by_amount(driver):
    driver.get("https://selenium.dev/selenium/web/scrolling_tests/frame_with_nested_scrolling_frame.html")
    # 创建从视窗坐标(10,10)开始的滚动源
    scroll_origin = ScrollOrigin.from_viewport(10, 10)
    # 从坐标点垂直滚动200px
    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, 200)\
        .perform()

    sleep(0.5)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)
    checkbox = driver.find_element(By.NAME, "scroll_checkbox")
    assert _in_viewport(driver, checkbox)


def _in_viewport(driver, element):  # 辅助函数：检测元素是否在可视区域内
    script = (  # JavaScript脚本：计算元素位置并判断是否在视窗内
        "for(var e=arguments[0],f=e.offsetTop,t=e.offsetLeft,o=e.offsetWidth,n=e.offsetHeight;\n"
        "e.offsetParent;)f+=(e=e.offsetParent).offsetTop,t+=e.offsetLeft;\n"
        "return f<window.pageYOffset+window.innerHeight&&t<window.pageXOffset+window.innerWidth&&f+n>\n"
        "window.pageYOffset&&t+o>window.pageXOffset"
    )
    return driver.execute_script(script, element)
