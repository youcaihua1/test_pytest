import pytest


def test_example(pytestconfig):
    print(pytestconfig.inicfg)  # 打印所有配置文件内容


def test_cli_args(pytestconfig):
    driver = pytestconfig.getoption("--driver")
    assert driver == "Edge"  # 验证命令行参数值


def test_plugins(pytestconfig):
    plugins = pytestconfig.pluginmanager.list_name_plugin()
    print("已加载插件:", plugins)


def test_data_path(pytestconfig):
    rootdir = pytestconfig.rootpath  # 项目根目录
    data_file = rootdir / "conftest.py"
    print(data_file)
    assert data_file.exists()



