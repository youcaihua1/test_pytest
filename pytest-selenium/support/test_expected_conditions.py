"""
模块名称: test_expected_conditions.py

功能描述:
    该模块的目标：学习和使用预期条件
    
主要函数:
    # =============================================================================
    # 常用预期条件参考表
    # -----------------------------------------------------------------------------
    # 函数名称                          | 描述
    # =============================================================================
    # title_is(title)                  | 检查页面标题是否等于给定字符串
    # title_contains(partial_title)   | 检查页面标题是否包含给定子串
    # presence_of_element_located(loc) | 检查元素存在于DOM中(不要求可见)
    # visibility_of_element_located(loc) | 检查元素存在且可见
    # visibility_of(element)           | 检查已知元素是否可见(元素已找到)
    # invisibility_of_element_located(loc) | 检查元素不可见或不存在
    # element_to_be_clickable(loc)     | 检查元素可见且启用(可点击)
    # element_to_be_selected(element)   | 检查单选框/复选框已被选中
    # element_located_to_be_selected(loc) | 检查定位到的元素已被选中
    # staleness_of(element)            | 检查元素已从DOM中移除
    # text_to_be_present_in_element(loc, text) | 检查元素文本包含给定文本
    # text_to_be_present_in_element_value(loc, value) | 检查元素值属性包含给定文本
    # frame_to_be_available_and_switch_to_it(loc) | 检查框架可用并切换到它
    # alert_is_present()               | 检查弹窗存在
    # new_window_is_opened(current_windows) | 检查有新窗口打开
    # number_of_windows_to_be(num)     | 检查窗口数量为指定数量
    # =============================================================================

    # =============================================================================
    # 参数说明：
    #   loc    -> 定位元组，如：(By.ID, 'element_id')
    #   title  -> 预期的标题字符串
    #   text   -> 预期的文本内容
    #   value  -> 预期的元素value属性值
    #   element -> 已找到的WebElement对象
    #   current_windows -> 当前打开的窗口句柄列表
    #   num    -> 预期的数量
    # =============================================================================

    
使用示例:
    > pytest -n 0 test_expected_conditions.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 预期条件API文档链接:
# https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html


def test_expected_condition(driver):
    driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
    revealed = driver.find_element(By.ID, "revealed")
    driver.find_element(By.ID, "reveal").click()

    wait = WebDriverWait(driver, timeout=2)
    wait.until(EC.visibility_of_element_located((By.ID, "revealed")))  # 使用显式等待 - 直到revealed元素变为可见状态

    revealed.send_keys("Displayed")
    assert revealed.get_property("value") == "Displayed"
