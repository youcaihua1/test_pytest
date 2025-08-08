"""
模块名称: first_script.py

功能描述:
    检查浏览器能否正常启动。

主要函数:


使用示例:
    >>> python first_script.py

作者: ych
邮箱:
创建日期: 2025-08-08
修改历史:
"""

from selenium import webdriver

driver = webdriver.Chrome()  # 若配置正确，无需参数即可启动
driver.get("https://www.baidu.com")
print(driver.title)  # 应输出 "百度一下，你就知道"
driver.quit()  # 关闭浏览器
