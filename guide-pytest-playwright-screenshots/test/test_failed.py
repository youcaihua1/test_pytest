def test_passed(page):
    page.goto('https://allurereport.org/docs/guides/playwright-pytest-screenshots/')
    assert "Allure" in page.title()


def test_failed(page):
    page.goto('https://allurereport.org/docs/guides/playwright-pytest-screenshots/')
    assert "pytest" in page.title()


def test_failed_2(page):
    page.goto(
        'https://allurereport.org/docs/guides/playwright-pytest-screenshots/#_2-screenshots-with-playwright-pytest')
    print(page.title())
    assert "pytest" in page.title()
