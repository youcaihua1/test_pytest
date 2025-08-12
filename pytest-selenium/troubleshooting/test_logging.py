"""
模块名称: test_logging.py

功能描述:
    该模块的目标：学习日志系统的基本配置和使用，包括日志级别设置、模块化控制，以及日志内容验证。
    
主要函数:
    
    
使用示例:
    > pytest -n 0 test_logging.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
import logging


def test_logging(log_path):
    """定义日志测试函数，接收日志文件路径参数"""
    logger = logging.getLogger('selenium')  # 获取名为'selenium'的日志记录器

    logger.setLevel(logging.DEBUG)  # 设置日志记录级别为DEBUG（捕获所有级别日志）

    handler = logging.FileHandler(log_path)  # 创建文件处理器，指定日志文件路径
    logger.addHandler(handler)  # 将文件处理器添加到日志记录器

    # 设置'selenium.webdriver.remote'日志记录器的级别为WARN（只记录警告及以上级别）
    logging.getLogger('selenium.webdriver.remote').setLevel(logging.WARN)
    # 设置'selenium.webdriver.common'日志记录器的级别为DEBUG（记录所有级别）
    logging.getLogger('selenium.webdriver.common').setLevel(logging.DEBUG)
    # 记录不同级别的日志信息
    logger.info("this is useful information")  # 信息级别
    logger.warning("this is a warning")  # 警告级别
    logger.debug("this is detailed debug information")  # 调试级别

    with open(log_path, 'r') as fp:
        assert len(fp.readlines()) == 3
