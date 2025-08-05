# pytest测试实战

- 代码来源：https://pragprog.com/titles/bopytest/python-testing-with-pytest/

- 学习的教程：《Python Testing with pytest》

### 对应章节内容：

ch1 pytest 入门
- 获取 pytest
- 运行 pytest
- 仅运行一个测试
- 使用命令行选项

ch2 编写测试函数
- 测试一个包
- 使用 assert 语句
- 预期异常
- 标记测试函数
- 跳过测试
- 将测试标记为预期失败
- 运行测试子集
- 参数化测试

ch3 pytest 夹具
- 通过 conftest.py 共享夹具
- 使用夹具进行设置和拆卸
- 使用 –setup-show 跟踪夹具执行
- 使用夹具提供测试数据
- 使用多个夹具
- 指定夹具作用域
- 使用 usefixtures 指定夹具
- 使用 autouse 设置始终使用的夹具
- 重命名夹具
- 参数化夹具

ch4 内置夹具
- 使用 tmpdir 和 tmpdir_factory
- 使用 pytestconfig
- 使用 cache
- 使用 capsys
- 使用 monkeypatch
- 使用 doctest_namespace
- 使用 recwarn

ch5 插件
- 查找插件
- 安装插件
- 编写你自己的插件
- 创建可安装的插件
- 测试插件
- 创建分发包

ch6 配置
- 理解 pytest 配置文件
- 更改默认命令行选项
- 注册标记以避免标记拼写错误
- 要求最低 pytest 版本
- 阻止 pytest 在错误位置查找
- 指定测试目录位置
- 更改测试发现规则
- 禁止 XPASS
- 避免文件名冲突

ch7 将 pytest 与其他工具结合使用
- pdb：调试测试失败
- Coverage.py：确定有多少代码被测试
- mock：替换系统的部分功能
- tox：测试多种配置
- Jenkins CI：自动化你的自动化测试
- unittest：使用 pytest 运行遗留测试

