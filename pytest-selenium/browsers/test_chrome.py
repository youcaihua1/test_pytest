"""
模块名称: test_chrome.py

功能描述:
    该模块的目标：学习以及应用特定于 Google Chrome 浏览器的功能和特性
    
主要函数:
    
    
使用示例:
    > pytest test_chrome.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/8
修改历史:
    1. 2025/8/8 - 创建文件
"""
import os
import re
import subprocess
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

chromedriver_bin = r'D:\Programs\driver\chromedriver-win64\chromedriver.exe'  # chromedriver安装路径
chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # 具体的Chrome安装路径


def test_basic_options():
    options = get_default_chrome_options()
    driver = webdriver.Chrome(options=options)
    driver.quit()


def test_args():
    options = get_default_chrome_options()

    options.add_argument("--start-maximized")  # 添加最大化窗口参数

    driver = webdriver.Chrome(options=options)
    driver.get('http://selenium.dev')

    driver.quit()


def test_set_browser_location():
    options = get_default_chrome_options()

    options.binary_location = chrome_bin  # 自定义浏览器路径

    driver = webdriver.Chrome(options=options)
    driver.quit()


def test_add_extension():  # 测试浏览器扩展安装
    options = get_default_chrome_options()
    script_dir = Path(__file__).resolve().parent  # 获取当前脚本所在目录
    extension_file_path = script_dir / "extensions" / "webextensions-selenium-example.crx"  # 扩展文件所在路径

    options.add_extension(str(extension_file_path))  # 添加扩展
    # CRX文件是Google Chrome浏览器扩展程序（Extension）的专用安装包格式。
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.selenium.dev/selenium/web/blank.html")
    driver.quit()


def test_keep_browser_open():
    options = get_default_chrome_options()

    options.add_experimental_option("detach", True)  # 添加实验性选项
    # WebDriver 进程不会主动终止浏览器，浏览器窗口会持续保持打开状态
    driver = webdriver.Chrome(options=options)
    driver.get('http://selenium.dev')
    driver.quit()  # 如果没有driver.quit()，浏览器将不会关闭。
    # driver.quit()是WebDriver的主动关闭命令，优先级高于所有保持打开的配置选项


def test_exclude_switches():  # exclude:排除
    options = get_default_chrome_options()

    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    # 禁用 Chrome 的“禁用弹窗拦截”功能，允许弹窗打开
    driver = webdriver.Chrome(options=options)
    driver.get('http://selenium.dev')
    driver.quit()


def test_log_to_file(log_path):
    service = webdriver.ChromeService(log_output=log_path)
    # 将 ChromeDriver 的日志输出到指定文件中
    driver = webdriver.Chrome(service=service)
    print(log_path)  # 可在allure中查看其文件名称
    with open(log_path, 'r') as fp:
        assert "Starting ChromeDriver" in fp.readline()

    driver.quit()


def test_log_to_stdout(capfd):
    service = webdriver.ChromeService(log_output=subprocess.STDOUT)
    # 将 ChromeDriver 的日志输出到标准输出（stdout）
    driver = webdriver.Chrome(service=service)

    out, err = capfd.readouterr()
    assert "Starting ChromeDriver" in out
    driver.quit()


def test_log_level(capfd):
    service = webdriver.ChromeService(service_args=['--log-level=DEBUG'], log_output=subprocess.STDOUT)
    # 设置 ChromeDriver 日志级别为 DEBUG，用于更详细的日志输出
    driver = webdriver.Chrome(service=service)

    out, err = capfd.readouterr()
    assert '[DEBUG]' in err
    driver.quit()


def test_log_features(log_path):
    service = webdriver.ChromeService(service_args=['--append-log', '--readable-timestamp'], log_output=log_path)
    # 启用日志的“追加模式”和“可读时间戳”功能
    driver = webdriver.Chrome(service=service)
    print(log_path)  # 可在allure中查看其文件名称
    with open(log_path, 'r') as f:
        assert re.match(r"\[\d\d-\d\d-\d\d\d\d", f.read())

    driver.quit()


def test_build_checks(capfd):
    service = webdriver.ChromeService(service_args=['--disable-build-check'], log_output=subprocess.STDOUT)
    # 禁用 ChromeDriver 的构建版本兼容性检查（不推荐，仅用于测试）
    driver = webdriver.Chrome(service=service)

    expected = "[WARNING]: You are using an unsupported command-line switch: --disable-build-check"
    out, err = capfd.readouterr()
    assert expected in err
    driver.quit()


def test_set_network_conditions():
    driver = webdriver.Chrome()
    # 模拟慢速网络环境（如 2Mbps 下载/上传，20ms 延迟）
    network_conditions = {
        "offline": False,
        "latency": 20,  # 20 ms of latency
        "download_throughput": 2000 * 1024 / 8,  # 2000 kbps
        "upload_throughput": 2000 * 1024 / 8,  # 2000 kbps
    }
    driver.set_network_conditions(**network_conditions)

    driver.get("https://www.selenium.dev")

    # check whether the network conditions are set
    assert driver.get_network_conditions() == network_conditions
    driver.quit()


def test_set_permissions():
    driver = webdriver.Chrome()
    driver.get('https://www.selenium.dev')

    driver.set_permissions('camera', 'denied')  # 设置浏览器权限，例如拒绝摄像头访问

    assert get_permission_state(driver, 'camera') == 'denied'
    driver.quit()


def get_permission_state(driver, name):
    """Helper function to query the permission state."""
    script = """
    const callback = arguments[arguments.length - 1];
    navigator.permissions.query({name: arguments[0]}).then(permissionStatus => {
        callback(permissionStatus.state);
    });
    """  # 执行异步 JS 脚本，获取指定权限（如 camera）的当前状态
    return driver.execute_async_script(script, name)


def test_cast_features():
    driver = webdriver.Chrome()

    try:
        sinks = driver.get_sinks()  # 测试 Chrome 的投屏（Cast）功能：获取设备、开始/停止投屏
        if sinks:
            sink_name = sinks[0]['name']
            driver.start_tab_mirroring(sink_name)
            driver.stop_casting(sink_name)
        else:
            pytest.skip("No available Cast sinks to test with.")
    finally:
        driver.quit()


def test_get_browser_logs():  # 获取浏览器控制台日志，验证是否有特定错误信息输出
    driver = webdriver.Chrome()
    driver.get("https://www.selenium.dev/selenium/web/bidi/logEntryAdded.html")
    driver.find_element(By.ID, "consoleError").click()

    logs = driver.get_log("browser")

    # Assert that at least one log contains the expected message
    assert any("I am console error" in log['message'] for log in logs), "No matching log message found."
    driver.quit()


def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # 禁用沙盒
    return options
