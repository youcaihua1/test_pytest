"""
模块名称: test_remote_webdriver.py

功能描述:
    该模块的目标：
    
主要函数:
    
    
使用示例:
    >>> 

作者: ych
创建日期: 2025/8/8
修改历史:
    1. 2025/8/8 - 创建文件
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.support.wait import WebDriverWait


def test_start_remote(server):
    options = get_default_chrome_options()
    driver = webdriver.Remote(command_executor=server, options=options)

    assert "localhost" in driver.command_executor._client_config.remote_server_addr
    driver.quit()


def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    return options