"""
模块名称: test_using_best_practice.py

功能描述:
    该模块的目标：
        这是一个结合 Python + pytest + Selenium 的示例代码
        实现了 "Action Bot", "Loadable Component" 和 "Page Object" 三种设计模式
说明:
    # 1. 三层架构设计：
    # - Action Bot：封装底层 Selenium 操作（ActionBot类）
    # - Loadable Component：处理页面加载逻辑（LoadableComponent抽象类）
    # - Page Object：封装页面功能和元素（TodoPage类）

    # 2. 可重用组件：
    # - ActionBot提供健壮的交互方法（带等待和错误处理）
    # - LoadableComponent确保页面加载状态可靠性
    # - 定位器生成方法支持动态查询

使用示例:
    > pytest -n 0 test_using_best_practice.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
import allure
import pytest
from selenium import webdriver
from selenium.common import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)  # 导入可能会遇到的异常类型
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="function")
def chrome_driver():
    with webdriver.Chrome() as driver:
        driver.set_window_size(1024, 768)
        driver.implicitly_wait(0.5)
        yield driver


class ActionBot:  # 定义 ActionBot 类，封装常用的浏览器操作
    def __init__(self, driver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=2,  # 每2秒检查一次条件
            ignored_exceptions=[  # 忽略的异常类型
                NoSuchElementException,
                StaleElementReferenceException,
                ElementNotInteractableException,
            ],
        )

    def element(self, locator: tuple) -> WebElement:  # 等待元素可交互状态，然后返回元素对象
        self.wait.until(lambda driver: driver.find_element(*locator))
        return self.driver.find_element(*locator)

    def elements(self, locator: tuple) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    def hover(self, locator: tuple) -> None:  # 模拟鼠标悬停在元素上
        element = self.element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def click(self, locator: tuple) -> None:
        element = self.element(locator)
        element.click()

    def type(self, locator: tuple, value: str) -> None:  # 在元素中输入文本
        element = self.element(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator: tuple) -> str:  # 获取元素的文本内容
        element = self.element(locator)
        return element.text


class LoadableComponent:  # 定义 LoadableComponent 抽象类
    def load(self):  # 抽象方法：加载组件/页面
        raise NotImplementedError("Subclasses must implement this method")

    def is_loaded(self):  # 抽象方法：检查组件/页面是否已加载
        raise NotImplementedError("Subclasses must implement this method")

    def get(self):  # 获取加载好的组件/页面
        if not self.is_loaded():  # 如果未加载，则加载它
            self.load()
        if not self.is_loaded():
            raise Exception("Page not loaded properly.")  # 加载失败抛出异常
        return self


class TodoPage(LoadableComponent):  # TodoPage 类实现 LoadableComponent 接口，代表待办事项页面
    url = "https://todomvc.com/examples/react/dist/"

    # 定义页面元素定位器
    new_todo_by = (By.CSS_SELECTOR, "input.new-todo")
    count_todo_left_by = (By.CSS_SELECTOR, "span.todo-count")
    todo_items_by = (By.CSS_SELECTOR, "ul.todo-list>li")

    # 视图切换链接定位器
    view_all_by = (By.LINK_TEXT, "All")
    view_active_by = (By.LINK_TEXT, "Active")
    view_completed_by = (By.LINK_TEXT, "Completed")

    # 主要操作元素定位器
    toggle_all_by = (By.CSS_SELECTOR, "input.toggle-all")
    clear_completed_by = (By.CSS_SELECTOR, "button.clear-completed")

    # 根据待办内容创建定位器的工具方法
    @staticmethod
    def build_todo_by(s: str) -> tuple:
        p = f"//li[.//label[contains(text(), '{s}')]]"
        return By.XPATH, p

    @staticmethod
    def build_todo_item_label_by(s: str) -> tuple:
        p = f"//label[contains(text(), '{s}')]"
        return By.XPATH, p

    @staticmethod
    def build_todo_item_toggle_by(s: str) -> tuple:
        by, using = TodoPage.build_todo_item_label_by(s)
        p = f"{using}/../input[@class='toggle']"
        return by, p

    @staticmethod
    def build_todo_item_delete_by(s: str) -> tuple:
        by, using = TodoPage.build_todo_item_label_by(s)
        p = f"{using}/../button[@class='destroy']"
        return by, p

    # 构造剩余待办数提示文本的工具方法
    def build_count_todo_left(self, count: int) -> str:
        if count == 1:
            return "1 item left!"
        else:
            return f"{count} items left!"

    def __init__(self, driver):
        self.driver = driver
        self.bot = ActionBot(driver)  # 创建ActionBot实例操作页面元素

    def load(self):  # 实现加载方法
        self.driver.get(self.url)

    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.new_todo_by))
            return True
        except:
            return False

    # 以下是页面的业务功能方法
    def count_todo_items_left(self) -> str:  # 获取剩余待办数量的文本
        return self.bot.text(self.count_todo_left_by)

    def todo_count(self) -> int:  # 获取待办项目的总数量
        return len(self.bot.elements(self.todo_items_by))

    def new_todo(self, s: str):  # 创建新的待办事项
        self.bot.type(self.new_todo_by, s + "\n")

    def toggle_todo(self, s: str):  # 切换待办事项的完成状态
        self.bot.click(self.build_todo_item_toggle_by(s))

    def hover_todo(self, s: str) -> None:  # 鼠标悬停在待办事项上（显示删除按钮）
        self.bot.hover(self.build_todo_by(s))

    def delete_todo(self, s: str):  # 删除指定待办事项
        self.hover_todo(s)  # 先悬停显示删除按钮
        self.bot.click(self.build_todo_item_delete_by(s))  # 点击删除按钮

    def clear_completed_todo(self):
        self.bot.click(self.clear_completed_by)  # 清除所有已完成的待办事项

    def toggle_all_todo(self):
        self.bot.click(self.toggle_all_by)  # 切换所有待办事项的状态（全选/取消全选）

    def view_all_todo(self):  # 显示所有待办事项
        self.bot.click(self.view_all_by)

    def view_active_todo(self):  # 显示活动（未完成）的待办事项
        self.bot.click(self.view_active_by)

    def view_completed_todo(self):  # 显示已完成的待办事项
        self.bot.click(self.view_completed_by)


@pytest.fixture
def page(chrome_driver) -> TodoPage:
    driver = chrome_driver
    return TodoPage(driver).get()


class TestTodoPage:
    @allure.title('测试创建待办事项功能')
    def test_new_todo(self, page: TodoPage):
        assert page.todo_count() == 0  # 初始应无待办事项
        page.new_todo("aaa")
        assert page.count_todo_items_left() == page.build_count_todo_left(1)

    @allure.title('测试切换待办状态功能')
    def test_todo_toggle(self, page: TodoPage):
        s = "aaa"
        page.new_todo(s)
        assert page.count_todo_items_left() == page.build_count_todo_left(1)

        page.toggle_todo(s)  # 标记为完成
        assert page.count_todo_items_left() == page.build_count_todo_left(0)

        page.toggle_todo(s)  # 取消完成状态
        assert page.count_todo_items_left() == page.build_count_todo_left(1)

    @allure.title('测试删除待办事项功能')
    def test_todo_delete(self, page: TodoPage):
        s1 = "aaa"
        s2 = "bbb"
        page.new_todo(s1)
        page.new_todo(s2)
        assert page.count_todo_items_left() == page.build_count_todo_left(2)

        page.delete_todo(s1)  # 删除第一个
        assert page.count_todo_items_left() == page.build_count_todo_left(1)

        page.delete_todo(s2)  # 删除第二个
        assert page.todo_count() == 0

    @allure.title('测试创建多个待办事项')
    def test_new_100_todo(self, page: TodoPage):
        for i in range(100):
            s = f"ToDo{i}"
            page.new_todo(s)
        assert page.count_todo_items_left() == page.build_count_todo_left(100)

    @allure.title('测试全选功能')
    def test_toggle_all_todo(self, page: TodoPage):
        for i in range(10):
            s = f"ToDo{i}"
            page.new_todo(s)
        assert page.count_todo_items_left() == page.build_count_todo_left(10)
        assert page.todo_count() == 10

        page.toggle_all_todo()  # 全选完成
        assert page.count_todo_items_left() == page.build_count_todo_left(0)
        assert page.todo_count() == 10

        page.toggle_all_todo()  # 取消全选
        assert page.count_todo_items_left() == page.build_count_todo_left(10)
        assert page.todo_count() == 10

    @allure.title('测试清除已完成功能')
    def test_clear_completed_todo(self, page: TodoPage):
        for i in range(10):
            s = f"ToDo{i}"
            page.new_todo(s)
        assert page.count_todo_items_left() == page.build_count_todo_left(10)
        assert page.todo_count() == 10

        for i in range(5):
            s = f"ToDo{i}"
            page.toggle_todo(s)  # 完成前5项
        assert page.count_todo_items_left() == page.build_count_todo_left(5)
        assert page.todo_count() == 10

        page.clear_completed_todo()  # 清除已完成
        assert page.count_todo_items_left() == page.build_count_todo_left(5)
        assert page.todo_count() == 5

    @allure.title("测试视图切换功能")
    def test_view_todo(self, page: TodoPage):
        for i in range(10):
            s = f"ToDo{i}"
            page.new_todo(s)
        for i in range(4):
            s = f"ToDo{i}"
            page.toggle_todo(s)  # 完成前4项

        page.view_all_todo()  # 全部视图
        assert page.count_todo_items_left() == page.build_count_todo_left(6)
        assert page.todo_count() == 10

        page.view_active_todo()  # 活动视图
        assert page.count_todo_items_left() == page.build_count_todo_left(6)
        assert page.todo_count() == 6

        page.view_completed_todo()  # 已完成视图
        assert page.count_todo_items_left() == page.build_count_todo_left(6)
        assert page.todo_count() == 4
