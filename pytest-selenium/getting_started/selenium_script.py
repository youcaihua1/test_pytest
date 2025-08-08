"""
模块名称: selenium_script.py

功能描述:
    该模块的目标：使用selenium对浏览器的元素进行相应操作，并且提交表单。
    
相关文档:
    元素操作：https://www.yuque.com/u37693518/gcfu7m/gb97dhx9hbovlbu7
    元素定位：https://www.yuque.com/u37693518/gcfu7m/peteek34nq38uasf

使用示例:
    >>> python selenium_script.py

作者: ych
创建日期: 2025/8/8
修改历史:
    1. 2025/8/8 - 创建文件
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # 浏览器初始化

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(3)  # 隐式等待

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()  # 点击按钮 提交表单

message = driver.find_element(by=By.ID, value="message")
text = message.text

print(text)

driver.quit()
