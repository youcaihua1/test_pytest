"""
模块名称: test_mouse.py

功能描述:
    该模块的目标：学习和运用 Selenium中的鼠标操作功能，包括基本点击、拖放、悬停
    
主要函数/方法/属性:
    1. 鼠标按钮常量

    | 常量                | 描述     |
    |---------------------|----------|
    | MouseButton.LEFT    | 左键     |
    | MouseButton.MIDDLE  | 中键     |
    | MouseButton.RIGHT   | 右键     |
    | MouseButton.BACK    | 后退按钮 |
    | MouseButton.FORWARD | 前进按钮 |

    2. 拖放操作类型

    | 方法                              | 描述         | 适用场景       |
    |-----------------------------------|--------------|----------------|
    | drag_and_drop(source, target)     | 拖到目标元素 | 目标元素可见   |
    | drag_and_drop_by_offset(source, x, y) | 按偏移量拖放 | 目标位置无特定元素 |

    
使用示例:
    > pytest -n 12 test_mouse.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
import pytest
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 导入等待条件


def test_click_and_hold(driver):
    """测试点击并保持操作"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.ID, "clickable")

    # 创建动作链：点击并保持
    # 点击并保持按住
    # 执行动作
    ActionChains(driver) \
        .click_and_hold(clickable) \
        .perform()

    sleep(0.5)
    assert driver.find_element(By.ID, "click-status").text == "focused"


def test_click_and_release(driver):
    """测试点击并释放操作"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.ID, "click")
    ActionChains(driver) \
        .click(clickable) \
        .perform()

    assert "resultPage.html" in driver.current_url


def test_right_click(driver):
    """测试右键点击操作"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.ID, "clickable")
    # 创建动作链：右键点击
    ActionChains(driver) \
        .context_click(clickable) \
        .perform()

    sleep(0.5)
    assert driver.find_element(By.ID, "click-status").text == "context-clicked"


def test_back_click_ab(driver):
    """测试鼠标后退按钮"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')
    driver.find_element(By.ID, "click").click()
    assert driver.title == "We Arrive Here"

    action = ActionBuilder(driver)
    # 模拟鼠标后退按钮按下和释放
    action.pointer_action.pointer_down(MouseButton.BACK)  # 按下后退按钮
    action.pointer_action.pointer_up(MouseButton.BACK)  # 释放后退按钮
    action.perform()

    assert driver.title == "BasicMouseInterfaceTest"


def test_forward_click_ab(driver):
    """测试鼠标前进按钮"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')
    driver.find_element(By.ID, "click").click()
    driver.back()  # 使用浏览器后退功能返回
    assert driver.title == "BasicMouseInterfaceTest"

    action = ActionBuilder(driver)
    action.pointer_action.pointer_down(MouseButton.FORWARD)  # 按下前进按钮
    action.pointer_action.pointer_up(MouseButton.FORWARD)  # 释放前进按钮
    action.perform()

    assert driver.title == "We Arrive Here"


def test_double_click(driver):
    """测试双击操作"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.ID, "clickable")
    # 创建动作链：双击元素
    ActionChains(driver) \
        .double_click(clickable) \
        .perform()

    assert driver.find_element(By.ID, "click-status").text == "double-clicked"


def test_hover(driver):
    """测试鼠标悬停"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    hoverable = driver.find_element(By.ID, "hover")
    # 创建动作链：移动鼠标到元素
    ActionChains(driver) \
        .move_to_element(hoverable) \
        .perform()

    assert driver.find_element(By.ID, "move-status").text == "hovered"


def test_move_by_offset_from_element(driver):
    """从元素位置偏移移动"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    mouse_tracker = driver.find_element(By.ID, "mouse-tracker")
    # 创建动作链：从元素位置偏移移动鼠标
    # 从元素位置向右偏移8像素
    ActionChains(driver) \
        .move_to_element_with_offset(mouse_tracker, 8, 0) \
        .perform()

    coordinates = driver.find_element(By.ID, "relative-location").text.split(", ")
    assert abs(int(coordinates[0]) - 100 - 8) < 2


def test_move_by_offset_from_viewport_origin_ab(driver):
    """从视口原点移动"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "absolute-location")))
    action = ActionBuilder(driver)
    action.pointer_action.move_to_location(8, 0)  # 移动到(8,0)坐标
    action.perform()

    coordinates = driver.find_element(By.ID, "absolute-location").text.split(", ")

    assert abs(int(coordinates[0]) - 8) < 2


def test_move_by_offset_from_current_pointer_ab(driver):
    """从当前位置偏移移动"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    action = ActionBuilder(driver)
    action.pointer_action.move_to_location(6, 3)  # 移动到(6,3)坐标
    action.perform()
    # 创建动作链：从当前位置偏移移动
    # 从当前位置偏移(13,15)像素
    ActionChains(driver) \
        .move_by_offset(13, 15) \
        .perform()

    coordinates = driver.find_element(By.ID, "absolute-location").text.split(", ")

    assert abs(int(coordinates[0]) - 6 - 13) < 2
    assert abs(int(coordinates[1]) - 3 - 15) < 2


def test_drag_and_drop_onto_element(driver):
    """拖放元素到目标元素"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    draggable = driver.find_element(By.ID, "draggable")
    droppable = driver.find_element(By.ID, "droppable")
    # 创建动作链：拖放元素到目标元素
    ActionChains(driver) \
        .drag_and_drop(draggable, droppable) \
        .perform()

    assert driver.find_element(By.ID, "drop-status").text == "dropped"


def test_drag_and_drop_by_offset(driver):
    """通过偏移量拖放元素"""
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    draggable = driver.find_element(By.ID, "draggable")
    start = draggable.location  # 起始位置
    finish = driver.find_element(By.ID, "droppable").location  # 目标位置
    # 创建动作链：通过偏移量拖放元素
    ActionChains(driver) \
        .drag_and_drop_by_offset(draggable, finish['x'] - start['x'], finish['y'] - start['y']) \
        .perform()

    assert driver.find_element(By.ID, "drop-status").text == "dropped"
