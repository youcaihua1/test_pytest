"""
模块名称: test_waits.py

功能描述:
    该模块的目标：模块展示了 Selenium 中处理动态元素的不同策略.
    
笔记:
   https://www.yuque.com/u37693518/gcfu7m/qciyvf19qaz29hdf
    
使用示例:
    > pytest -n 5 test_waits.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import pytest
import time
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_fails(driver):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(By.ID, "adder").click()  # 点击添加元素的按钮（会触发元素创建但需要时间）

    with pytest.raises(NoSuchElementException):
        driver.find_element(By.ID, 'box0')  # 尝试立即查找新创建的元素（此时元素尚未出现）


def test_sleep(driver):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(By.ID, "adder").click()  # 点击添加元素的按钮

    time.sleep(2)  # 固定等待2秒（不推荐的方式,不够灵活）
    added = driver.find_element(By.ID, "box0")

    assert added.get_dom_attribute('class') == "redbox"


def test_implicit(driver):
    """
    Selenium 内置了一种自动等待元素出现的方式, 称为 隐式等待 .
    隐式等待的值可以通过浏览器选项中的 timeouts 设置来设定, 也可以通过驱动程序的方法来设定 (如下所示) .

    这是一个全局设置, 适用于整个会话期间的每个元素定位调用. 默认值为 0 , 这意味着如果未找到元素, 将立即返回错误. 如果设置了隐式等待, 驱动程序将在返回错误之前等待所提供的时长. 请注意, 一旦定位到元素, 驱动程序将返回元素引用, 代码将继续执行, 因此较大的隐式等待值不一定增加会话的持续时间.

    警告: 请勿混合使用隐式等待和显式等待.
    这样做可能会导致等待时间不可预测. 例如, 设置 10 秒的隐式等待和 15 秒的显式等待,
    可能会导致在 20 秒后发生超时.
    """
    driver.implicitly_wait(2)  # 设置全局隐式等待时间为2秒
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(By.ID, "adder").click()

    added = driver.find_element(By.ID, "box0")

    assert added.get_dom_attribute('class') == "redbox"


def test_explicit(driver):
    """
        显式等待 是在代码中添加的, 用于轮询应用程序的循环, 直到特定条件评估为真时, 才退出循环并继续执行代码中的下一个命令. 如果在指定的超时值之前条件未满足, 代码将给出超时错误. 由于应用程序未处于所需状态的方式有很多, 因此显式等待是为每个需要等待的地方指定确切等待条件的绝佳选择.
        另一个不错的特性是, 默认情况下, Selenium 等待类会自动等待指定的元素存在.
    """
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    revealed = driver.find_element(By.ID, "revealed")  # 获取将被显示的元素（初始状态不可见）
    driver.find_element(By.ID, "reveal").click()

    wait = WebDriverWait(driver, timeout=2)  # 创建显式等待对象（最长等待2秒）
    wait.until(lambda _: revealed.is_displayed())  # 等待直到元素可见（自定义等待条件）

    revealed.send_keys("Displayed")
    assert revealed.get_property("value") == "Displayed"


def test_explicit_options(driver):
    """
    Wait 类可以通过各种参数进行实例化, 这些参数会改变条件的评估方式.

    这可以包括：

    - 更改代码的评估频率 (轮询间隔)
    - 指定哪些异常应自动处理
    - 更改总超时时长
    - 自定义超时消息

    例如, 如果默认情况下对 元素不可交互 错误进行重试,
    那么我们可以在执行中的代码里的某个方法内添加一个操作 (我们只需要确保代码在成功时返回 true 即可)：
    """
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    revealed = driver.find_element(By.ID, "revealed")
    driver.find_element(By.ID, "reveal").click()

    errors = [NoSuchElementException, ElementNotInteractableException]  # 定义要忽略的异常列表

    # 创建带配置的显式等待对象：
    # - timeout=2: 最长等待2秒
    # - poll_frequency=.2: 每0.2秒检查一次条件
    # - ignored_exceptions=errors: 忽略指定异常
    wait = WebDriverWait(driver, timeout=2, poll_frequency=.2, ignored_exceptions=errors)
    wait.until(lambda _: revealed.send_keys("Displayed") or True)  # 尝试发送文本，不管结果如何都会返回True

    assert revealed.get_property("value") == "Displayed"
