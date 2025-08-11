"""
模块名称: conftest.py

作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import pytest
import logging
import os

from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='function')
def log_path():
    pid = os.getpid()  # 获取当前进程ID（解决在分布式测试中多个进程同时访问同一日志文件导致的错误）
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    log_path = f"log_file_{suffix}_pid{pid}.log"

    yield log_path  # 将路径交给测试函数使用

    # 测试结束后执行以下清理
    # 清理日志系统
    logger = logging.getLogger('selenium')
    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.close()

    os.remove(log_path)  # 删除日志文件


@pytest.fixture(scope='function')
def driver(request):
    chrome_options = Options()  # 创建 Chrome 选项对象
    chrome_options.add_argument("--headless=new")  # 添加无头模式参数

    service = webdriver.ChromeService(r'D:\Programs\driver\chromedriver-win64\chromedriver.exe')  # 手动指定 ChromeDriver 位置

    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
