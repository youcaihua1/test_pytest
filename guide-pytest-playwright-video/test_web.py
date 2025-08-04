import allure
from playwright.sync_api import expect


@allure.title("Page should have a word in the title")
def test_main_page_title_should_have_word_in_title(page):
    with allure.step("Open the main page"):
        page.goto("https://en.wikipedia.org/wiki/Software_testing")

    with allure.step("Look for a phrase in the title"):
        expect(page).to_have_title("Bad title")


@allure.title("Page should have a text entry element")
def test_main_page_should_have_text_entry(page):
    with allure.step("Open the main page"):
        page.goto("https://en.wikipedia.org/wiki/Software_testing")

    with allure.step("Find an element on the page"):
        elem = page.get_by_role("search")
        expect(elem).to_have_role("no-role")
