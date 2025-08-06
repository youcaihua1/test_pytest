import re
import os
import allure
import pytest
from pathlib import Path

SCREENSHOT_NAME_PATTERN = re.compile(r"^test-failed-\d+\.png$")  # 匹配截图文件
VIDEO_NAME_PATTERN = re.compile(r".*\.webm$")  # 匹配视频文件


# 在失败的测试中添加截图和视频
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    # 检查测试是否失败
    if hasattr(item, "rep_call") and item.rep_call.failed:
        try:
            # 1. 获取当前测试的唯一标识符
            # 将::替换为-
            test_name = item.nodeid.replace("::", "-").replace(".", "-").replace("/", "-").replace("_", "-").replace(
                "[", "-").replace("]", "")

            # 2. 构建当前测试的截图目录路径
            artifacts_dir = Path("test-results") / f"{test_name}"

            # 3. 只查找当前测试的截图目录
            if artifacts_dir.exists() and artifacts_dir.is_dir():
                for file in artifacts_dir.iterdir():
                    if file.is_file() and SCREENSHOT_NAME_PATTERN.match(file.name):
                        # 4. 附加截图到Allure
                        allure.attach.file(
                            str(file),
                            name=file.name,
                            attachment_type=allure.attachment_type.PNG,
                        )
                    if file.is_file() and VIDEO_NAME_PATTERN.match(file.name):
                        # 4. 附加视频到Allure
                        allure.attach.file(
                            str(file),
                            name=file.name,
                            attachment_type=allure.attachment_type.WEBM,
                        )
        except Exception as e:
            print(f"Error attaching screenshot: {e}")


# 捕获测试结果
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep
