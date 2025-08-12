"""
模块名称: test_options.py

功能描述:
    该模块的目标：了解并且使用常用的浏览器选项
    
主要函数:
    
    
使用示例:
    > pytest test_options.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/8
修改历史:
    1. 2025/8/8 - 创建文件
"""
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType


def test_page_load_strategy_normal():
    options = get_default_chrome_options()
    options.page_load_strategy = 'normal'  # 设置页面加载策略 - normal，等待整个页面（包括所有依赖资源）完全加载
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_page_load_strategy_eager():
    options = get_default_chrome_options()
    options.page_load_strategy = 'eager'  # 设置页面加载策略 - eager，仅等待 HTML 解析完成
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_page_load_strategy_none():
    options = get_default_chrome_options()
    options.page_load_strategy = 'none'  # 设置页面加载策略 - none，导航命令后立即继续执行
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_timeouts_script():
    options = get_default_chrome_options()
    options.timeouts = {'script': 5000}  # 设置异步JavaScript脚本 (execute_async_script()) 的最大执行等待时间，单位是毫秒
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_timeouts_page_load():
    options = get_default_chrome_options()
    options.timeouts = {'pageLoad': 5000}  # 配置 Selenium WebDriver 的页面加载超时时间，单位是毫秒（5000ms = 5秒）
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_timeouts_implicit_wait():
    options = get_default_chrome_options()
    options.timeouts = {'implicit': 5000}  # 设置全局的元素查找超时，影响所有 find_element和 find_elements方法
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_unhandled_prompt():
    options = get_default_chrome_options()
    options.unhandled_prompt_behavior = 'accept'  # 自动接受所有未处理的 JavaScript 弹窗,
    # 当出现 alert()、confirm()或 prompt()时自动点击"确定", 防止弹窗阻塞自动化流程
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_strict_file_interactability():
    options = get_default_chrome_options()
    options.strict_file_interactability = True
    # 启用文件交互的严格模式（默认值通常为 False）
    # 强制要求文件输入元素（<input type="file">）必须：
    #   在视口中完全可见
    #   未被其他元素遮挡
    #   未被禁用（disabled属性）
    #   可以接收焦点
    # 不符合条件时，拒绝执行文件上传操作
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_proxy():
    options = get_default_chrome_options()
    options.proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http.proxy:1234'})
    # 配置浏览器通过代理服务器访问网络
    # proxyType  ProxyType.MANUAL  使用手动配置的代理
    # httpProxy  'http.proxy:1234'  HTTP 代理地址和端口
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_set_browser_name():
    options = get_default_chrome_options()
    assert options.capabilities['browserName'] == 'chrome'  # options.capabilities['browserName'] 告知 Selenium 需要启动哪种浏览器
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_set_browser_version():
    options = get_default_chrome_options()
    options.browser_version = 'stable'  # 指定浏览器版本
    assert options.capabilities['browserVersion'] == 'stable'  # browserVersion 版本
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_platform_name():
    options = get_default_chrome_options()
    options.platform_name = 'any'  # 告知 Selenium 服务器（特别是 Grid 或云测试平台）不限制测试运行的操作系统，让调度系统自动选择可用的平台。
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def test_accept_insecure_certs():
    options = get_default_chrome_options()
    options.accept_insecure_certs = True
    # 用于绕过 HTTPS 证书安全验证的关键设置，让测试脚本能够访问使用无效 SSL 证书的网站（自签名证书、过期证书、域名不匹配等）
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/")
    driver.quit()


def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # 禁用 Chrome 的沙盒（Sandbox）安全机制。
    options.add_argument("--headless=new")  # 启用无头模式
    return options
