"""
模块名称: test_cookies.py

功能描述:
    该模块的目标：使用Cookie管理的核心功能
    
主要函数:
    driver.add_cookie()  # 添加Cookie

    driver.get_cookie("name")  # 获取单个Cookie
    driver.get_cookies()  # 获取所有Cookie

    driver.delete_cookie("name")  # 删除单个Cookie
    driver.delete_all_cookies()  # 删除所有Cookie

    WebDriver中Cookie操作的参数属性说明

    | 属性       | 类型     | 说明                      | 示例                   |
    |-----------|----------|--------------------------|-----------------------|
    | `name`    | 字符串    | Cookie名称               | `"session_id"`       |
    | `value`   | 字符串    | Cookie值                 | `"abc123"`           |
    | `domain`  | 字符串    | 所属域名                 | `".example.com"`      |
    | `path`    | 字符串    | 有效路径                 | `"/admin"`            |
    | `expiry`  | 整数      | 过期时间(Unix时间戳)     | `1672531200 (2023-01-01)` |
    | `secure`  | 布尔      | 是否仅HTTPS发送          | `True/False`          |
    | `httpOnly`| 布尔      | 是否仅HTTP访问           | `True/False`          |
    | `sameSite`| 字符串    | 跨站请求策略             | `"Strict"`, `"Lax"`, `"None"` |

使用示例:
    >>> pytest -n 6 test_cookies.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
from selenium import webdriver


def test_add_cookie(driver):
    driver.get("http://www.example.com")

    # 添加Cookie到当前浏览器上下文
    # 参数：包含name和value的字典
    driver.add_cookie({"name": "key", "value": "value"})


def test_get_named_cookie(driver):
    driver.get("http://www.example.com")

    # 添加一个Cookie
    driver.add_cookie({"name": "foo", "value": "bar"})

    # 获取名为'foo'的Cookie详情
    # 返回包含所有Cookie属性的字典
    print(driver.get_cookie("foo"))


def test_get_all_cookies(driver):
    driver.get("http://www.example.com")
    # 添加两个Cookie
    driver.add_cookie({"name": "test1", "value": "cookie1"})
    driver.add_cookie({"name": "test2", "value": "cookie2"})

    # 获取当前域名的所有Cookie
    # 返回Cookie字典的列表
    print(driver.get_cookies())


def test_delete_cookie(driver):
    driver.get("http://www.example.com")

    driver.add_cookie({"name": "test1", "value": "cookie1"})
    driver.add_cookie({"name": "test2", "value": "cookie2"})

    # 删除名为'test1'的Cookie
    driver.delete_cookie("test1")


def test_delete_all_cookies(driver):
    driver.get("http://www.example.com")

    driver.add_cookie({"name": "test1", "value": "cookie1"})
    driver.add_cookie({"name": "test2", "value": "cookie2"})

    # 删除当前域名的所有Cookie
    driver.delete_all_cookies()


def test_same_side_cookie_attr(driver):
    driver.get("http://www.example.com")

    # 添加两个具有SameSite属性的Cookie
    # SameSite属性控制Cookie是否随跨站请求发送
    # 'Strict': 完全禁止跨站发送
    # 'Lax': 允许部分安全跨站请求发送
    driver.add_cookie({"name": "foo", "value": "value", "sameSite": "Strict"})
    driver.add_cookie({"name": "foo1", "value": "value", "sameSite": "Lax"})

    cookie1 = driver.get_cookie("foo")
    cookie2 = driver.get_cookie("foo1")

    print(cookie1)
    print(cookie2)
