"""
模块名称: test_locators.py

功能描述:
    该模块的目标：学习以及运用元素选择策略。
    
元素选择策略:
    在 WebDriver 中有 8 种不同的内置元素定位策略：

    定位器 Locator	    描述
    class name	        定位class属性与搜索值匹配的元素（不允许使用复合类名）
    css selector	    定位 CSS 选择器匹配的元素
    id	                定位 id 属性与搜索值匹配的元素
    name	            定位 name 属性与搜索值匹配的元素
    link text	        定位link text可视文本与搜索值完全匹配的锚元素
    partial link text	定位link text可视文本部分与搜索值部分匹配的锚点元素。如果匹配多个元素，则只选择第一个元素。
    tag name	        定位标签名称与搜索值匹配的元素
    xpath	            定位与 XPath 表达式匹配的元素
    
使用示例:
    >>> pytest -n 8 test_locators.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_class_name(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.CLASS_NAME, "information")  # 通过class name定位元素

    assert element is not None
    assert element.tag_name == "input"


def test_css_selector(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.CSS_SELECTOR, "#fname")  # 通过CSS选择器定位元素

    assert element is not None
    assert element.get_attribute("value") == "Jane"


def test_id(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.ID, "lname")  # 通过ID定位元素

    assert element is not None
    assert element.get_attribute("value") == "Doe"


def test_name(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.NAME, "newsletter")  # 通过name属性定位元素

    assert element is not None
    assert element.tag_name == "input"


def test_link_text(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.LINK_TEXT, "Selenium Official Page")  # 通过链接文本定位元素

    assert element is not None
    assert element.get_attribute("href") == "https://www.selenium.dev/"


def test_partial_link_text(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.PARTIAL_LINK_TEXT, "Official Page")  # 通过部分链接文本定位元素

    assert element is not None
    assert element.get_attribute("href") == "https://www.selenium.dev/"


def test_tag_name(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.TAG_NAME, "a")  # 通过标签名定位元素（定位第一个<a>标签）

    assert element is not None
    assert element.get_attribute("href") == "https://www.selenium.dev/"


def test_xpath(driver):
    driver.get("https://www.selenium.dev/selenium/web/locators_tests/locators.html")
    element = driver.find_element(By.XPATH, "//input[@value='f']")  # 通过XPath定位元素

    assert element is not None
    assert element.get_attribute("type") == "radio"
