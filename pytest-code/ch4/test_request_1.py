import pytest


def test_example(request):
    """获取测试信息（成员属性）"""
    print(f"测试节点: {request.node}")
    print(f"测试函数/方法的名字: {request.node.name}")
    print(f"测试所在的模块: {request.module.__name__}")
    print(f"测试函数对象: {request.function}")
    if request.cls:
        print(f"Test class: {request.cls.__name__}")
    print(f"全局 pytest 配置对象: {request.config}")
    print(f"pytest 会话对象: {request.session}")


@pytest.fixture(params=["apple", "banana"])
def fruit(request):  # 通过 request.param 获取参数值
    return request.param  # 依次返回 "apple"、"banana"


@pytest.mark.parametrize("color", ["red", "blue"])
def test_fruit_and_color(fruit, color):
    """
    A request object gives access to the requesting test context
    and has a param attribute in case the fixture is parametrized.
    翻译：request 对象提供对请求测试上下文的访问，并在夹具参数化的情况下具有 param 属性。
    """
    print(f"Combination: {fruit} + {color}")


@pytest.fixture
def database_fixture():
    return "connect_db"


def test_dynamic_fixture(request):
    """动态调用其他 fixture"""
    db = request.getfixturevalue("database_fixture")  # 动态调用 database_fixture 夹具
    assert db == "connect_db"


def test_markers(request):
    """访问测试函数上的标记"""
    slow_marker = request.node.get_closest_marker("slow")
    print(slow_marker)


@pytest.mark.slow
def test_markers_slow(request):
    """访问测试函数上的标记"""
    slow_marker = request.node.get_closest_marker("slow")
    print(slow_marker)

