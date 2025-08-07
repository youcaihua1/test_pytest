import sys
import pytest
import random


def greeting(name):
    print('Hi, {}'.format(name))


def test_greeting(capsys):
    greeting('Earthling')
    out, err = capsys.readouterr()
    assert out == 'Hi, Earthling\n'
    assert err == ''

    greeting('Brian')
    greeting('Nerd')
    out, err = capsys.readouterr()
    assert out == 'Hi, Brian\nHi, Nerd\n'
    assert err == ''


def yikes(problem):
    print('YIKES! {}'.format(problem), file=sys.stderr)


def test_yikes(capsys):
    yikes('Out of coffee!')
    out, err = capsys.readouterr()
    assert out == ''
    assert 'Out of coffee!' in err


def test_capsys_disabled(capsys):
    with capsys.disabled():
        print('\nalways print this')
    print('normal print, usually captured')


@pytest.mark.parametrize('i', range(40))
def test_for_fun(i, capsys):
    if random.randint(1, 10) == 2:
        with capsys.disabled():
            sys.stdout.write('F')


def function_prints():
    print("Hello stdout")
    print("Warning: something happened", file=sys.stderr)


def test_capsys_basic(capsys):
    """capsys夹具 基本用法示例"""
    function_prints()  # 调用被测试函数
    # 捕获输出
    captured = capsys.readouterr()
    # 断言标准输出
    assert captured.out == "Hello stdout\n"
    # 断言标准错误
    assert captured.err == "Warning: something happened\n"


def test_multiple_captures(capsys):
    """capsys夹具 多次调用测试"""
    print("First call")
    captured1 = capsys.readouterr()  # 捕获后重置缓冲区
    assert captured1.out == "First call\n"

    print("Second call")
    captured2 = capsys.readouterr()  # 只捕获第二次输出
    assert captured2.out == "Second call\n"


def test_disable_capture(capsys):
    """通过 capsys.disabled() 上下文管理器，临时允许输出显示（如调试时）"""
    print("This is captured")  # 会被捕获
    with capsys.disabled():
        print("This prints directly to console")  # 绕过捕获，直接输出到终端
    print("Captured again")  # 重新被捕获
    captured = capsys.readouterr()
