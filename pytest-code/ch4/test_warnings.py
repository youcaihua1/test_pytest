import warnings
import allure
import pytest


def lame_function():
    warnings.warn("Please stop using this", DeprecationWarning)
    # rest of function


def test_lame_function(recwarn):
    lame_function()
    assert len(recwarn) == 1
    w = recwarn.pop()
    assert w.category == DeprecationWarning
    assert str(w.message) == 'Please stop using this'


def test_lame_function_2():
    # pytest.warns(None)  # 不应该使用 None
    # 1 所有警告必须是Warning的子类
    # 2 警告消息必须是字符串类型
    # 3 None不满足以上任一要求，导致类型错误
    with pytest.warns(DeprecationWarning) as warning_list:
        lame_function()

    assert len(warning_list) == 1
    w = warning_list.pop()
    assert w.category == DeprecationWarning
    assert str(w.message) == 'Please stop using this'


def test_warning_capture(recwarn):
    # 触发一个警告
    warnings.warn("This is a deprecation warning", DeprecationWarning)
    # 1. 检查警告数量
    assert len(recwarn) == 1
    # 2. 获取警告对象
    warning = recwarn.pop()
    # 3. 检查警告类型
    assert warning.category == DeprecationWarning
    # 4. 检查警告消息内容
    assert "deprecation warning" in str(warning.message)
    # 警告被取出后列表清空
    assert len(recwarn) == 0


def test_list_property(recwarn):
    # recwarn.list
    # 作用：访问捕获的警告列表
    # 特点：按警告触发顺序存储
    warnings.warn("First warning")
    warnings.warn("Second warning")

    assert len(recwarn.list) == 2
    assert "First" in str(recwarn.list[0].message)


def test_warning_order(recwarn):
    # recwarn.pop
    # 作用：取出并移除指定类型的警告

    # 触发三个同类型警告
    warnings.warn("First warning", UserWarning)
    warnings.warn("Second warning", UserWarning)
    warnings.warn("Third warning", UserWarning)
    # 同时触发一个其他类型的警告
    warnings.warn("Deprecation warning", DeprecationWarning)
    # 按触发顺序弹出
    w1 = recwarn.pop(UserWarning)
    w2 = recwarn.pop(UserWarning)
    # 断言警告内容
    assert str(w1.message) == "First warning"
    assert str(w2.message) == "Second warning"
    # 剩下的警告列表
    remaining = recwarn.list
    assert len(remaining) == 2
    assert str(remaining[0].message) == "Third warning"
    assert str(remaining[1].message) == "Deprecation warning"
    # 弹出最后一个UserWarning
    w3 = recwarn.pop(UserWarning)
    assert str(w3.message) == "Third warning"
    # 弹出DeprecationWarning
    dep_warn = recwarn.pop(DeprecationWarning)
    assert str(dep_warn.message) == "Deprecation warning"
    # 清空后应该没有警告
    assert len(recwarn) == 0


def test_warning_attributes(recwarn):
    def generate_warning():
        warnings.warn("Line-specific warning", UserWarning)

    generate_warning()
    w = recwarn.pop(UserWarning)
    print(
        f'警告消息对象         {w.message}\n',
        f'警告类别            {w.category}\n',
        f'触发警告的文件路径    {w.filename}\n',
        f'触发警告的行号       {w.lineno}\n',
        f'触发警告的源代码行    {w.line}\n',
        f'触发警告的源代码对象  {w.source}\n',
    )


@allure.id("WARNING-001")
def test_ignore_resource_warning(recwarn):
    # 忽略特定类型的警告
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.warn("Ignored warning", ResourceWarning)
    # 确认没有捕获 ResourceWarning
    with pytest.raises(AssertionError):
        recwarn.pop(ResourceWarning)
    # 其他警告仍被捕获
    warnings.warn("Should be captured")
    assert len(recwarn) == 1
