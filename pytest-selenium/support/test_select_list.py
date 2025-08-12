"""
模块名称: test_select_list.py

功能描述:
    该模块的目标：处理HTML表单中常见的下拉选择框（单选框和多选框），以及如何处理特殊场景（如禁用选项）。
    
主要函数:
    1、 Select 类功能 ：

    select_by_visible_text(): 通过选项文本选择
    select_by_value(): 通过选项值选择
    select_by_index(): 通过索引选择
    deselect_by_value(): 通过值取消选择（仅多选框）
    options: 获取所有选项
    all_selected_options: 获取当前选中的选项
    
使用示例:
    > pytest -n 3 test_select_list.py
    先运行pytest后 在运行下面命令：
    > allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    > allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/12
修改历史:
    1. 2025/8/12 - 创建文件
"""
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 导入Select类用于处理下拉菜单


@allure.title('测试选择框选项功能')
def test_select_options(driver):
    """测试选择框选项功能"""
    driver.get('https://selenium.dev/selenium/web/formPage.html')

    select_element = driver.find_element(By.NAME, 'selectomatic')
    select = Select(select_element)  # 创建Select对象来操作选择框
    # 定位选择框中的各个选项
    two_element = driver.find_element(By.CSS_SELECTOR, 'option[value=two]')
    four_element = driver.find_element(By.CSS_SELECTOR, 'option[value=four]')
    count_element = driver.find_element(By.CSS_SELECTOR, "option[value='still learning how to count, apparently']")
    # 通过可见文本选择选项
    select.select_by_visible_text('Four')
    assert four_element.is_selected()
    # 通过值选择选项
    select.select_by_value('two')
    assert two_element.is_selected()
    # 通过索引选择选项（索引从0开始）
    select.select_by_index(3)
    assert count_element.is_selected()


def test_select_multiple_options(driver):
    """测试多选选择框功能"""
    driver.get('https://selenium.dev/selenium/web/formPage.html')
    select_element = driver.find_element(By.NAME, 'multi')  # 定位多选选择框
    select = Select(select_element)
    # 定位各个选项
    ham_element = driver.find_element(By.CSS_SELECTOR, 'option[value=ham]')
    gravy_element = driver.find_element(By.CSS_SELECTOR, "option[value='onion gravy']")
    egg_element = driver.find_element(By.CSS_SELECTOR, 'option[value=eggs]')
    sausage_element = driver.find_element(By.CSS_SELECTOR, "option[value='sausages']")

    option_elements = select_element.find_elements(By.TAG_NAME, 'option')  # 获取选择框中的所有选项
    option_list = select.options  # 使用Select的options属性获取所有选项
    assert option_elements == option_list

    selected_option_list = select.all_selected_options  # 获取当前选中的所有选项
    expected_selection = [egg_element, sausage_element]  # 页面初始选中的选项
    assert selected_option_list == expected_selection
    # 选择新选项
    select.select_by_value('ham')
    select.select_by_value('onion gravy')
    assert ham_element.is_selected()
    assert gravy_element.is_selected()
    # 取消选择初始选项
    select.deselect_by_value('eggs')
    select.deselect_by_value('sausages')
    assert not egg_element.is_selected()
    assert not sausage_element.is_selected()


def test_disabled_options(driver):
    """测试禁用选项的功能"""
    driver.get('https://selenium.dev/selenium/web/formPage.html')

    select_element = driver.find_element(By.NAME, 'single_disabled')
    select = Select(select_element)
    # 使用pytest验证选择禁用选项会引发异常
    # NotImplementedError是Selenium对尝试选择禁用选项的响应
    with pytest.raises(NotImplementedError):
        select.select_by_value('disabled')
