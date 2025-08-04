def test_example(selenium):
    selenium.get("https://www.selenium.dev/")
    selenium.save_screenshot("img/screenshot.png")
    try:
        assert "Selenium" in selenium.title
    except AssertionError:
        selenium.save_screenshot("img/screenshot.png")
        raise
