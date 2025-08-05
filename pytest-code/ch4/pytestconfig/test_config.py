import pytest


def test_option(pytestconfig):
    print('"foo" set to:', pytestconfig.getoption('foo'))
    print('"myopt" set to:', pytestconfig.getoption('myopt'))


# pytestconfig 是 session 作用域 的夹具，不能在函数作用域的夹具中直接请求（需通过高阶夹具传递）
# 所以下面的两个夹具不能这样写，会导致test_pytestconfig测试函数报错
# @pytest.fixture()
# def foo(pytestconfig):
#     return pytestconfig.option.foo
#
#
# @pytest.fixture()
# def myopt(pytestconfig):
#     return pytestconfig.option.myopt
#
# 修改1：使用request.config，如test_legacy测试函数
# 修改2：提升作用域，将foo夹具修改成session作用域的
@pytest.fixture(scope="session")
def foo(pytestconfig):
    return pytestconfig.option.foo


# 修改3：使用中间层，
@pytest.fixture(scope="session")
def global_config(pytestconfig):
    return pytestconfig


@pytest.fixture()
def myopt(global_config):
    return global_config.option.myopt


def test_fixtures_for_options(foo, myopt):
    print('"foo" set to:', foo)
    print('"myopt" set to:', myopt)


def test_pytestconfig(pytestconfig):
    print('args            :', pytestconfig.args)
    print('inifile         :', pytestconfig.inifile)
    print('invocation_dir  :', pytestconfig.invocation_dir)
    print('rootdir         :', pytestconfig.rootdir)
    print('-k EXPRESSION   :', pytestconfig.getoption('keyword'))
    print('-v, --verbose   :', pytestconfig.getoption('verbose'))
    print('-q, --quiet     :', pytestconfig.getoption('quiet'))
    print('-l, --showlocals:', pytestconfig.getoption('showlocals'))
    print('--tb=style      :', pytestconfig.getoption('tbstyle'))


def test_legacy(request):
    print('\n"foo" set to:', request.config.getoption('foo'))
    print('"myopt" set to:', request.config.getoption('myopt'))
    print('"keyword" set to:', request.config.getoption('keyword'))
