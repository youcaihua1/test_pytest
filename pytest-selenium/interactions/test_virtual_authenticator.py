"""
模块名称: test_virtual_authenticator.py

功能描述:
    这个测试套件涵盖了Selenium虚拟认证器（Virtual Authenticator）功能的各个方面：

    ========================================================================
    功能领域                 | 功能点
    ------------------------|------------------------------------------------
    1. 虚拟认证器选项配置     | 测试创建和配置虚拟认证器选项
                            | 验证选项属性设置
    ------------------------|------------------------------------------------
    2. 认证器生命周期管理     | 添加虚拟认证器
                            | 移除虚拟认证器
    ------------------------|------------------------------------------------
    3. 凭证管理              | 创建和添加 resident key (可驻留密钥)
                            | 创建和添加 non-resident key (非驻留密钥)
                            | 获取凭证列表
                            | 移除单个凭证
                            | 移除所有凭证
    ------------------------|------------------------------------------------
    4. 错误处理             | 测试在 U2F 协议下添加 resident key 应抛出异常
    ------------------------|------------------------------------------------
    5. 属性验证              | 验证用户验证状态设置
    ========================================================================


    
    
使用示例:
    >>> pytest -n 10 test_virtual_authenticator.py
    先运行pytest后 在运行下面命令：
    >>> allure generate ./allure -o ./allure-report --clean (这个需要在项目根目录下运行)
    >>> allure open ./allure-report (这个需要在项目根目录下运行)
作者: ych
创建日期: 2025/8/11
修改历史:
    1. 2025/8/11 - 创建文件
"""
import pytest
from base64 import urlsafe_b64decode, urlsafe_b64encode

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.virtual_authenticator import (
    Credential,
    VirtualAuthenticatorOptions,
)

BASE64__ENCODED_PK = '''
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDbBOu5Lhs4vpowbCnmCyLUpIE7JM9sm9QXzye2G+jr+Kr
MsinWohEce47BFPJlTaDzHSvOW2eeunBO89ZcvvVc8RLz4qyQ8rO98xS1jtgqi1NcBPETDrtzthODu/gd0sjB2Tk3TLuBGV
oPXt54a+Oo4JbBJ6h3s0+5eAfGplCbSNq6hN3Jh9YOTw5ZA6GCEy5l8zBaOgjXytd2v2OdSVoEDNiNQRkjJd2rmS2oi9AyQ
FR3B7BrPSiDlCcITZFOWgLF5C31Wp/PSHwQhlnh7/6YhnE2y9tzsUvzx0wJXrBADW13+oMxrneDK3WGbxTNYgIi1PvSqXlq
GjHtCK+R2QkXAgMBAAECggEAVc6bu7VAnP6v0gDOeX4razv4FX/adCao9ZsHZ+WPX8PQxtmWYqykH5CY4TSfsuizAgyPuQ0
+j4Vjssr9VODLqFoanspT6YXsvaKanncUYbasNgUJnfnLnw3an2XpU2XdmXTNYckCPRX9nsAAURWT3/n9ljc/XYY22ecYxM
8sDWnHu2uKZ1B7M3X60bQYL5T/lVXkKdD6xgSNLeP4AkRx0H4egaop68hoW8FIwmDPVWYVAvo8etzWCtibRXz5FcNld9MgD
/Ai7ycKy4Q1KhX5GBFI79MVVaHkSQfxPHpr7/XcmpQOEAr+BMPon4s4vnKqAGdGB3j/E3d/+4F2swykoQKBgQD8hCsp6FIQ
5umJlk9/j/nGsMl85LgLaNVYpWlPRKPc54YNumtvj5vx1BG+zMbT7qIE3nmUPTCHP7qb5ERZG4CdMCS6S64/qzZEqijLCqe
pwj6j4fV5SyPWEcpxf6ehNdmcfgzVB3Wolfwh1ydhx/96L1jHJcTKchdJJzlfTvq8wwKBgQDeCnKws1t5GapfE1rmC/h4ol
L2qZTth9oQmbrXYohVnoqNFslDa43ePZwL9Jmd9kYb0axOTNMmyrP0NTj41uCfgDS0cJnNTc63ojKjegxHIyYDKRZNVUR/d
xAYB/vPfBYZUS7M89pO6LLsHhzS3qpu3/hppo/Uc/AM/r8PSflNHQKBgDnWgBh6OQncChPUlOLv9FMZPR1ZOfqLCYrjYEqi
uzGm6iKM13zXFO4AGAxu1P/IAd5BovFcTpg79Z8tWqZaUUwvscnl+cRlj+mMXAmdqCeO8VASOmqM1ml667axeZDIR867ZG8
K5V029Wg+4qtX5uFypNAAi6GfHkxIKrD04yOHAoGACdh4wXESi0oiDdkz3KOHPwIjn6BhZC7z8mx+pnJODU3cYukxv3WTct
lUhAsyjJiQ/0bK1yX87ulqFVgO0Knmh+wNajrb9wiONAJTMICG7tiWJOm7fW5cfTJwWkBwYADmkfTRmHDvqzQSSvoC2S7aa
9QulbC3C/qgGFNrcWgcT9kCgYAZTa1P9bFCDU7hJc2mHwJwAW7/FQKEJg8SL33KINpLwcR8fqaYOdAHWWz636osVEqosRrH
zJOGpf9x2RSWzQJ+dq8+6fACgfFZOVpN644+sAHfNPAI/gnNKU5OfUv+eav8fBnzlf1A3y3GIkyMyzFN3DE7e0n/lyqxE4H
BYGpI8g==
'''  # 预定义的一个Base64编码的私钥字符串，用于测试中创建凭证


@pytest.fixture(scope="module", autouse=True)
def driver():
    yield WebDriver()


def test_virtual_authenticator_options():
    options = VirtualAuthenticatorOptions()  # 创建虚拟认证器选项对象
    options.is_user_verified = True  # 用户是否已验证
    options.has_user_verification = True  # 是否支持用户验证
    options.is_user_consenting = True  # 用户是否同意
    options.transport = VirtualAuthenticatorOptions.Transport.USB  # 传输方式为USB
    options.protocol = VirtualAuthenticatorOptions.Protocol.U2F  # 协议为U2F
    options.has_resident_key = False  # 是否支持resident key（可驻留密钥）

    assert len(options.to_dict()) == 6


def test_add_authenticator(driver):
    # 创建虚拟认证器选项
    options = VirtualAuthenticatorOptions()
    options.protocol = VirtualAuthenticatorOptions.Protocol.U2F
    options.has_resident_key = False

    # 在驱动中添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 获取认证器中的凭证列表
    credential_list = driver.get_credentials()

    assert len(credential_list) == 0


def test_remove_authenticator(driver):
    # 创建默认虚拟认证器选项
    options = VirtualAuthenticatorOptions()

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 移除虚拟认证器
    driver.remove_virtual_authenticator()
    assert driver.virtual_authenticator_id is None


def test_create_and_add_resident_key(driver):
    options = VirtualAuthenticatorOptions()
    options.protocol = VirtualAuthenticatorOptions.Protocol.CTAP2
    options.has_resident_key = True
    options.has_user_verification = True
    options.is_user_verified = True

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 准备resident credential（可驻留凭证）的参数
    credential_id = bytearray({1, 2, 3, 4})  # 凭证ID
    rp_id = "localhost"  # 依赖方ID
    user_handle = bytearray({1})  # 用户句柄
    privatekey = urlsafe_b64decode(BASE64__ENCODED_PK)  # 解码Base64编码的私钥
    sign_count = 0  # 签名计数

    # 创建resident credential
    resident_credential = Credential.create_resident_credential(credential_id, rp_id, user_handle, privatekey,
                                                                sign_count)

    # 将凭证添加到认证器
    driver.add_credential(resident_credential)

    # 获取认证器中的所有凭证
    credential_list = driver.get_credentials()
    assert len(credential_list) == 1


def test_add_resident_credential_not_supported_when_authenticator_uses_u2f_protocol(driver):
    # 创建虚拟认证器选项（U2F协议）
    options = VirtualAuthenticatorOptions()
    options.protocol = VirtualAuthenticatorOptions.Protocol.U2F
    options.has_resident_key = False

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 准备凭证参数
    credential_id = bytearray({1, 2, 3, 4})
    rp_id = "localhost"
    user_handle = bytearray({1})
    privatekey = urlsafe_b64decode(BASE64__ENCODED_PK)
    sign_count = 0

    # 创建resident credential
    credential = Credential.create_resident_credential(credential_id, rp_id, user_handle, privatekey, sign_count)

    # 预期会抛出InvalidArgumentException异常
    with pytest.raises(InvalidArgumentException):
        driver.add_credential(credential)  # 尝试添加凭证（U2F协议不支持resident key）


def test_create_and_add_non_resident_key(driver):
    # 创建虚拟认证器选项（U2F协议）
    options = VirtualAuthenticatorOptions()
    options.protocol = VirtualAuthenticatorOptions.Protocol.U2F
    options.has_resident_key = False

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 准备non-resident credential（非驻留凭证）的参数
    credential_id = bytearray({1, 2, 3, 4})
    rp_id = "localhost"
    privatekey = urlsafe_b64decode(BASE64__ENCODED_PK)  # 解码私钥
    sign_count = 0

    # 创建non-resident credential
    credential = Credential.create_non_resident_credential(credential_id, rp_id, privatekey, sign_count)

    # 添加凭证到认证器
    driver.add_credential(credential)

    # 获取所有凭证
    credential_list = driver.get_credentials()
    assert len(credential_list) == 1  # 验证凭证数量为1


def test_get_credential(driver):
    # 创建虚拟认证器选项（CTAP2协议）
    options = VirtualAuthenticatorOptions()
    options.protocol = VirtualAuthenticatorOptions.Protocol.CTAP2  # 协议为CTAP2
    options.has_resident_key = True  # 支持resident key
    options.has_user_verfied = True
    options.is_user_verified = True  # 用户已通过验证

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 准备resident credential参数
    credential_id = bytearray({1, 2, 3, 4})
    rp_id = "localhost"
    user_handle = bytearray({1})
    privatekey = urlsafe_b64decode(BASE64__ENCODED_PK)
    sign_count = 0

    # 创建resident credential
    credential = Credential.create_resident_credential(credential_id, rp_id, user_handle, privatekey, sign_count)

    # 添加凭证到认证器
    driver.add_credential(credential)

    # 获取所有凭证
    credential_list = driver.get_credentials()

    assert len(credential_list) == 1
    assert credential_list[0].id == urlsafe_b64encode(credential_id).decode()  # 验证凭证ID（Base64编码后）是否匹配


def test_remove_credential(driver):
    # 创建默认虚拟认证器选项
    options = VirtualAuthenticatorOptions()

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 准备non-resident credential参数
    credential_id = bytearray({1, 2, 3, 4})
    rp_id = "localhost"
    privatekey = urlsafe_b64decode(BASE64__ENCODED_PK)
    sign_count = 0

    # 创建non-resident credential
    credential = Credential.create_non_resident_credential(credential_id, rp_id, privatekey, sign_count)

    # 添加凭证到认证器
    driver.add_credential(credential)

    # 移除凭证（使用凭证ID）
    driver.remove_credential(credential.id)

    # 也可以使用字节数组形式的凭证ID移除
    # driver.remove_credential(credential_id)

    # 验证凭证已被移除
    assert len(driver.get_credentials()) == 0


def test_remove_all_credentials(driver):
    # 创建虚拟认证器选项（支持resident key）
    options = VirtualAuthenticatorOptions()
    options.has_resident_key = True

    # 添加虚拟认证器
    driver.add_virtual_authenticator(options)

    # 准备resident credential参数
    credential_id = bytearray({1, 2, 3, 4})
    rp_id = "localhost"
    user_handle = bytearray({1})
    privatekey = urlsafe_b64decode(BASE64__ENCODED_PK)
    sign_count = 0

    # 创建resident credential
    resident_credential = Credential.create_resident_credential(credential_id, rp_id, user_handle, privatekey,
                                                                sign_count)

    # 添加凭证到认证器
    driver.add_credential(resident_credential)

    # 移除所有凭证
    driver.remove_all_credentials()

    assert len(driver.get_credentials()) == 0


def test_set_user_verified():
    # 创建虚拟认证器选项
    options = VirtualAuthenticatorOptions()
    options.is_user_verified = True  # 设置用户已通过验证

    assert options.to_dict().get("isUserVerified") is True
