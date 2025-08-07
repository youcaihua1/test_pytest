import os
import requests


def test_env_vars(monkeypatch):
    """
    夹具monkeypatch功能：环境变量管理
    """
    # 设置环境变量
    monkeypatch.setenv("API_KEY", "test_key")
    assert os.getenv("API_KEY") == "test_key"
    # 删除环境变量
    monkeypatch.delenv("API_KEY", raising=False)
    assert "API_KEY" not in os.environ


def test_mock_function(monkeypatch):
    """
    夹具monkeypatch功能：模块/对象属性修改
    """
    import utils
    from utils import Preferences

    # 临时修改函数返回值
    monkeypatch.setattr(utils, "get_version", lambda: "2.0.0")
    assert utils.get_version() == "2.0.0"

    # 模拟方法返回值
    monkeypatch.setattr(Preferences, "get_default_language", lambda: "zh-CN")
    assert Preferences.get_default_language() == "zh-CN"


def test_input_mocking(monkeypatch):
    """
    标准输入输出重定向
    """
    # 模拟用户输入
    inputs = iter(["John", "30"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    name = input("Name: ")
    age = input("Age: ")
    assert name == "John" and age == "30"


def test_api_call(monkeypatch):
    """模拟外部API调用"""
    # 创建模拟响应
    class MockResponse:
        status_code = 200

        def json(self):
            return {"data": "mocked"}

    # 替换requests.get方法
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    response = requests.get("https://api.example.com")
    assert response.json()["data"] == "mocked"





