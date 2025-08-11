"""
模块名称: test_frames.py

功能描述:
    该模块的目标：演示了Selenium中处理iframe的主要方法
    
    核心方法：
        ================================================================
        方法                              描述                使用场景
        -------------------------------- ------------------- -----------
        driver.switch_to.frame(          切换到指定          需要操作iframe内
          frame_reference)               iframe             元素时

        driver.switch_to.default_content() 返回主文档         完成iframe操作后

        driver.switch_to.parent_frame()  返回父级frame      多层嵌套iframe时
        ================================================================

    
    
使用示例:
    >>> pytest -n 0 test_frames.py
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


def test_frames(driver):
    driver.get("https://www.selenium.dev/selenium/web/iframes.html")

    # --- 使用ID切换iframe ---
    iframe = driver.find_element(By.ID, "iframe1")
    driver.switch_to.frame(iframe)  # 切换到该iframe
    assert "We Leave From Here" in driver.page_source

    email_element = driver.find_element(By.ID, "email")  # 在iframe内定位元素并操作
    email_element.send_keys("admin@selenium.dev")
    email_element.clear()
    driver.switch_to.default_content()  # 切换回主文档

    # --- 使用name切换iframe ---
    iframe1 = driver.find_element(By.NAME, "iframe1-name")  # 通过name属性定位iframe元素
    driver.switch_to.frame(iframe1)  # 切换到该iframe
    assert "We Leave From Here" in driver.page_source

    email = driver.find_element(By.ID, "email")
    email.send_keys("admin@selenium.dev")
    email.clear()
    driver.switch_to.default_content()

    # --- 使用索引切换iframe ---
    driver.switch_to.frame(0)  # 切换到页面中的第一个iframe（索引从0开始）
    assert "We Leave From Here" in driver.page_source

    # 切换回主文档
    driver.switch_to.default_content()
    assert "This page has iframes" in driver.page_source
