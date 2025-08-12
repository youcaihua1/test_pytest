"""
模块名称: test_service.py

功能描述:
    该模块的目标：验证 Selenium ChromeService 的不同配置方式
    
主要函数:
    
    
使用示例:
    > pytest test_service.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/8
修改历史:
    1. 2025/8/8 - 创建文件
"""
from selenium import webdriver


chromedriver_bin = r'D:\Programs\driver\chromedriver-win64\chromedriver.exe'  # chromedriver安装路径
chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # 具体的Chrome安装路径


def test_basic_service():
    service = webdriver.ChromeService()  # 不指定任何参数  依赖系统环境变量中的 ChromeDriver 路径
    driver = webdriver.Chrome(service=service)
    driver.quit()


def test_driver_location():  # 测试手动指定浏览器和驱动的安装路径
    options = get_default_chrome_options()
    options.binary_location = chrome_bin  # 具体的Chrome安装路径
    # 使用具体路径创建Service对象
    service = webdriver.ChromeService(executable_path=chromedriver_bin)

    driver = webdriver.Chrome(service=service, options=options)
    driver.quit()


def test_driver_port():  # 验证 ChromeDriver 能在指定端口启动服务
    service = webdriver.ChromeService(port=1234)  # 指定自定义端口

    driver = webdriver.Chrome(service=service)
    driver.quit()


def get_default_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # 禁用沙盒
    return options
