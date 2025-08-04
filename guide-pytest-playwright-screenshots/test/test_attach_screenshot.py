import allure
from pathlib import Path


# 附加页面或元素的屏幕截图
def test_attach_screenshot(page, path="img/screenshot.png"):
    name = Path(path).name
    page.goto("https://playwright.dev/")
    page.screenshot(path=path)
    allure.attach.file(
        path,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


# 无需将截图保存到磁盘
# 附加页面或元素的屏幕截图
def test_attach_screenshot_2(page, name='screenshot-2'):
    page.goto(
        "https://allurereport.org/docs/guides/playwright-pytest-screenshots/#_2-screenshots-with-playwright-pytest")
    allure.attach(
        page.screenshot(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
