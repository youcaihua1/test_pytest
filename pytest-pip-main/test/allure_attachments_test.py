import json
import os

import allure
from allure import attachment_type
from loguru import logger


def test_attach():
    allure.attach.file(os.path.join("..", "resources", "allure-logo.png"), name="PNG example",
                       attachment_type=attachment_type.PNG)

    allure.attach("<h1>Example html attachment</h1>", name="HTML example", attachment_type=attachment_type.HTML)
    allure.attach("Some text content", name="TXT example", attachment_type=attachment_type.TEXT)
    allure.attach('first,second,third\none,two,three', name="CSV example", attachment_type=attachment_type.CSV)
    allure.attach(json.dumps({"first": 1, "second": 2}, indent=2),
                  name="JSON example", attachment_type=attachment_type.JSON)
    allure.attach("\n".join(["https://github.com/allure-framework", "https://github.com/allure-examples"]),
                  name="URI List example", attachment_type=attachment_type.URI_LIST)
    # TODO Screen diff


def test_log():
    """基础使用"""
    logger.debug("调试信息")
    logger.info("业务提示")
    logger.info("详细提示")
    logger.warning("警告提醒")
    logger.error("错误追踪")
    logger.critical("致命错误")
    assert True
