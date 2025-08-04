def test_example(page):
    page.goto("https://playwright.dev/")
    page.screenshot(path="img/screenshot.png")
    try:
        assert "Playwright" in page.title()
    except AssertionError:
        page.screenshot(path="img/screenshot.png")
        raise
