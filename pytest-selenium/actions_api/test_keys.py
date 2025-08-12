"""
模块名称: test_keys.py

功能描述:
    该模块的目标：使用键盘操作，
    只有 2 个操作可以使用键盘完成: 按下某个键，以及释放一个按下的键.
    除了支持 ASCII 字符外，每个键盘按键还具有 可以按特定顺序按下或释放的表现形式.

主要函数:
    键盘操作基础
    | 方法名                     | 描述                   | 示例                         |
    |----------------------------|------------------------|------------------------------|
    | key_down(key)              | 按下按键               | .key_down(Keys.SHIFT)        |
    | key_up(key)                | 释放按键               | .key_up(Keys.SHIFT)          |
    | send_keys(keys)            | 发送按键               | .send_keys("abc")            |
    | send_keys_to_element(element, keys) | 向指定元素发送按键 | .send_keys_to_element(input, "text") |

    特殊按键常量
    | 按键常量           | 描述         |
    |--------------------|--------------|
    | Keys.SHIFT         | Shift键      |
    | Keys.CONTROL       | Control键    |
    | Keys.COMMAND       | Command键 (Mac) |
    | Keys.ALT           | Alt键        |
    | Keys.ARROW_LEFT    | 左箭头键     |
    | Keys.ARROW_RIGHT   | 右箭头键     |
    | Keys.ARROW_UP      | 上箭头键     |
    | Keys.ARROW_DOWN    | 下箭头键     |
    | Keys.ENTER         | 回车键       |
    | Keys.BACKSPACE     | 退格键       |

使用示例:
    > pytest -n 5 test_keys.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import sys

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By


def test_key_down(driver):
    driver.get('https://selenium.dev/selenium/web/single_text_input.html')

    # 创建操作链：
    # 按下Shift键
    # 输入小写字母abc（由于Shift按下会变成大写）
    # 执行操作链
    ActionChains(driver)\
        .key_down(Keys.SHIFT)\
        .send_keys("abc")\
        .perform()

    assert driver.find_element(By.ID, "textInput").get_attribute('value') == "ABC"


def test_key_up(driver):
    driver.get('https://selenium.dev/selenium/web/single_text_input.html')

    ActionChains(driver)\
        .key_down(Keys.SHIFT)\
        .send_keys("a")\
        .key_up(Keys.SHIFT)\
        .send_keys("b")\
        .perform()

    assert driver.find_element(By.ID, "textInput").get_attribute('value') == "Ab"


def test_send_keys_to_active_element(driver):
    driver.get('https://selenium.dev/selenium/web/single_text_input.html')

    ActionChains(driver)\
        .send_keys("abc")\
        .perform()

    assert driver.find_element(By.ID, "textInput").get_attribute('value') == "abc"


def test_send_keys_to_designated_element(driver):
    driver.get('https://selenium.dev/selenium/web/single_text_input.html')
    driver.find_element(By.TAG_NAME, "body").click()

    text_input = driver.find_element(By.ID, "textInput")
    ActionChains(driver)\
        .send_keys_to_element(text_input, "abc")\
        .perform()

    assert driver.find_element(By.ID, "textInput").get_attribute('value') == "abc"


def test_copy_and_paste(driver):
    driver.get('https://selenium.dev/selenium/web/single_text_input.html')
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL  # 根据操作系统确定修饰键（Mac用COMMAND，其他用CONTROL）

    # 创建复杂操作链：
    # 输入字符串"Selenium!"
    # 按左箭头键移动光标到!前
    # 按下Shift键
    # Shift+↑（全选单词Selenium）
    # 释放Shift键
    # 按下修饰键(Ctrl/Cmd)
    # 执行剪切(x)和两次粘贴(vv)
    # 释放修饰键
    # 执行操作链
    ActionChains(driver)\
        .send_keys("Selenium!")\
        .send_keys(Keys.ARROW_LEFT)\
        .key_down(Keys.SHIFT)\
        .send_keys(Keys.ARROW_UP)\
        .key_up(Keys.SHIFT)\
        .key_down(cmd_ctrl)\
        .send_keys("xvv")\
        .key_up(cmd_ctrl)\
        .perform()

    assert driver.find_element(By.ID, "textInput").get_attribute('value') == "SeleniumSelenium!"

