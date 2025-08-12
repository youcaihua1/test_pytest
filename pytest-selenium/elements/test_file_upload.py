"""
模块名称: test_file_upload.py

功能描述:
    该模块的目标：展示了Selenium文件上传的流程.
    
使用示例:
    > pytest -n 1 test_file_upload.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import os

from selenium import webdriver
from selenium.webdriver.common.by import By


def test_uploads(driver):
    """
    由于 Selenium 不能与文件上传对话框交互，
    因此它提供了一种无需打开对话框即可上传文件的方法。
    如果该元素是一个类型为 file 的 input 元素，
    则可以使用 send keys 方法发送将要上传文件的完整路径。
    """
    driver.get("https://the-internet.herokuapp.com/upload")

    # 构造要上传文件的绝对路径：
    # 1. os.path.dirname(__file__) 获取当前脚本所在目录
    # 2. os.path.join() 向上跳一级目录（".."） 然后进入img目录
    # 3. 定位到目标文件 "selenium-snapshot.png"
    # 4. os.path.abspath() 确保得到绝对路径
    upload_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "img", "selenium-snapshot.png"))

    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")  # 定位文件上传输入框（使用CSS选择器查找type="file"的input元素）
    file_input.send_keys(upload_file)  # 将文件路径发送到上传输入框（触发文件选择）
    driver.find_element(By.ID, "file-submit").click()  # 定位并点击提交按钮

    file_name_element = driver.find_element(By.ID, "uploaded-files")  # 定位显示上传文件名的元素
    file_name = file_name_element.text  # 获取上传成功后的文件名文本

    assert file_name == "selenium-snapshot.png"
