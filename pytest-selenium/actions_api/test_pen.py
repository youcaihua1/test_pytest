"""
模块名称: test_pen.py

功能描述:
    该模块的目标：使用Selenium的高级指针API来模拟笔输入设备
    
主要函数:
    
    
使用示例:
    > pytest -n 2 test_pen.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
import math

from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_PEN  # 导入笔指针类型常量
from selenium.webdriver.common.actions.pointer_input import PointerInput  # 导入指针输入类
from selenium.webdriver.common.by import By


def test_use_pen(driver):
    driver.get('https://www.selenium.dev/selenium/web/pointerActionsPage.html')

    pointer_area = driver.find_element(By.ID, "pointerArea")
    pen_input = PointerInput(POINTER_PEN, "default pen")  # 创建笔指针输入设备
    action = ActionBuilder(driver, mouse=pen_input)  # 创建动作构建器，指定使用笔指针

    # 构建笔指针动作序列：
    # 1. 移动笔到指针区域中心
    # 2. 按下笔
    # 3. 移动笔2像素（向右和向下）
    # 4. 抬起笔
    action.pointer_action \
        .move_to(pointer_area) \
        .pointer_down() \
        .move_by(2, 2) \
        .pointer_up()
    action.perform()
    # 获取页面记录的所有指针事件
    moves = driver.find_elements(By.CLASS_NAME, "pointermove")  # 移动事件
    move_to = properties(moves[0])  # 解析第一个移动事件属性
    down = properties(driver.find_element(By.CLASS_NAME, "pointerdown"))  # 按下事件属性
    move_by = properties(moves[1])  # 第二个移动事件属性
    up = properties(driver.find_element(By.CLASS_NAME, "pointerup"))  # 抬起事件属性
    # 计算指针区域的中心坐标
    rect = pointer_area.rect  # 获取元素位置和尺寸
    center_x = rect["x"] + rect["width"] / 2  # 中心X坐标
    center_y = rect["y"] + rect["height"] / 2  # 中心Y坐标

    assert move_to["button"] == "-1"
    assert move_to["pointerType"] == "pen"
    assert move_to["pageX"] == str(math.floor(center_x))
    assert move_to["pageY"] == str(math.floor(center_y))
    assert down["button"] == "0"
    assert down["pointerType"] == "pen"
    assert down["pageX"] == str(math.floor(center_x))
    assert down["pageY"] == str(math.floor(center_y))
    assert move_by["button"] == "-1"
    assert move_by["pointerType"] == "pen"
    assert move_by["pageX"] == str(math.floor(center_x + 2))
    assert move_by["pageY"] == str(math.floor(center_y + 2))
    assert up["button"] == "0"
    assert up["pointerType"] == "pen"
    assert up["pageX"] == str(math.floor(center_x + 2))
    assert up["pageY"] == str(math.floor(center_y + 2))


def test_set_pointer_event_properties(driver):
    driver.get('https://www.selenium.dev/selenium/web/pointerActionsPage.html')

    pointer_area = driver.find_element(By.ID, "pointerArea")
    pen_input = PointerInput(POINTER_PEN, "default pen")
    action = ActionBuilder(driver, mouse=pen_input)
    # 构建笔指针动作序列（带高级属性）：
    # 1. 移动笔到指针区域中心
    # 2. 按下笔
    # 3. 移动笔并设置倾斜和旋转
    # 4. 抬起笔（指定按钮0）
    action.pointer_action \
        .move_to(pointer_area) \
        .pointer_down() \
        .move_by(2, 2, tilt_x=-72, tilt_y=9, twist=86) \
        .pointer_up(0)
    action.perform()

    moves = driver.find_elements(By.CLASS_NAME, "pointermove")
    move_to = properties(moves[0])
    down = properties(driver.find_element(By.CLASS_NAME, "pointerdown"))
    move_by = properties(moves[1])
    up = properties(driver.find_element(By.CLASS_NAME, "pointerup"))

    rect = pointer_area.rect
    center_x = rect["x"] + rect["width"] / 2
    center_y = rect["y"] + rect["height"] / 2

    assert move_to["button"] == "-1"
    assert move_to["pointerType"] == "pen"
    assert move_to["pageX"] == str(math.floor(center_x))
    assert move_to["pageY"] == str(math.floor(center_y))
    assert down["button"] == "0"
    assert down["pointerType"] == "pen"
    assert down["pageX"] == str(math.floor(center_x))
    assert down["pageY"] == str(math.floor(center_y))
    assert move_by["button"] == "-1"
    assert move_by["pointerType"] == "pen"
    assert move_by["pageX"] == str(math.floor(center_x + 2))
    assert move_by["pageY"] == str(math.floor(center_y + 2))
    assert move_by["tiltX"] == "-72"
    assert move_by["tiltY"] == "9"
    assert move_by["twist"] == "86"
    assert up["button"] == "0"
    assert up["pointerType"] == "pen"
    assert up["pageX"] == str(math.floor(center_x + 2))
    assert up["pageY"] == str(math.floor(center_y + 2))


def properties(element):  # 辅助函数：解析事件属性
    """
    解析元素文本为属性字典
    示例输入: "pointerType: pen, pageX: 100, pageY: 200"
    输出: {'pointerType': 'pen', 'pageX': '100', 'pageY': '200'}
    """
    kv = element.text.split(' ', 1)[1].split(', ')
    return {x[0]: x[1] for x in list(map(lambda item: item.split(': '), kv))}
