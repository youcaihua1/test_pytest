"""
模块名称: test_actions.py

功能描述:
    该模块的目标：展示了Selenium高级用户交互功能的核心用法，对于测试复杂的用户交互场景（如拖放、组合键操作等）非常重要
    
主要函数/方法:
    1、 ActionChains：高级用户交互模拟器
    常用方法:

    | 方法名                 | 描述               | 示例                         |
    |------------------------|--------------------|------------------------------|
    | click(element)         | 点击元素           | .click(button)               |
    | double_click(element)  | 双击元素           | .double_click(icon)          |
    | drag_and_drop(source, target) | 拖放元素       | .drag_and_drop(item, trash)  |
    | send_keys(keys)        | 发送按键           | .send_keys(Keys.ENTER)       |
    | key_down(key)          | 按下按键           | .key_down(Keys.CONTROL)      |
    | key_up(key)            | 释放按键           | .key_up(Keys.CONTROL)        |
    | move_to_element(element)| 移动鼠标到元素     | .move_to_element(menu)       |
    | pause(seconds)         | 暂停执行           | .pause(1.5)                  |

    2、 ActionBuilder：底层输入设备控制器

    pointer = action_builder.add_pointer_input("mouse", "mouse1")  # 添加指针设备（鼠标）
    ActionBuilder(driver).clear_actions()  # 清除所有当前动作状态

    # 同时控制键盘和鼠标
    keyboard = action_builder.add_key_input("keyboard")
    mouse = action_builder.add_pointer_input("mouse", "mouse1")
    
使用示例:
    >>> pytest -n 2 test_actions.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
from time import time

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By


def test_pauses(driver):
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    start = time()

    clickable = driver.find_element(By.ID, "clickable")  # 定位可点击元素

    # 创建动作链并执行一系列操作：
    # 1. 移动鼠标到元素
    # 2. 暂停1秒
    # 3. 点击并按住鼠标
    # 4. 再次暂停1秒
    # 5. 输入文本"abc"
    # 执行整个动作链
    ActionChains(driver)\
        .move_to_element(clickable)\
        .pause(1)\
        .click_and_hold()\
        .pause(1)\
        .send_keys("abc")\
        .perform()

    duration = time() - start
    # 验证总耗时在2-3秒之间（包含2次1秒暂停）
    assert duration > 2
    assert duration < 3


def test_releases_all(driver):
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.ID, "clickable")

    # 创建第一个动作链：
    # 1. 点击并按住元素
    # 2. 按下Shift键
    # 3. 按下"a"键（此时应为大写A）
    # 执行动作链
    ActionChains(driver)\
        .click_and_hold(clickable)\
        .key_down(Keys.SHIFT)\
        .key_down("a")\
        .perform()

    ActionBuilder(driver).clear_actions()  # 使用ActionBuilder清除所有当前动作状态

    # 创建第二个动作链：
    # 按下"a"键（此时应为小写a）
    ActionChains(driver).key_down('a').perform()

    assert clickable.get_attribute('value')[0] == "A"
    assert clickable.get_attribute('value')[1] == "a"
