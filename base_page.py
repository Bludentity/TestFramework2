"""
Purpose: Abstract Playwright interactions behind a reusable BasePage class.
This class wraps common operations and adds logging-friendly semantics and timeouts.
"""
from playwright.sync_api import Page, expect
from typing import Union
import time


class BasePage:

    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout

    def maps_to(self, url: str):
        self.page.goto(url, wait_until='load')

    def click_element(self, locator: str):
        el = self.page.locator(locator)
        el.wait_for(state='visible', timeout=self.timeout)
        el.click()

    def input_text(self, locator: str, text: str, clear_first: bool = True):
        el = self.page.locator(locator)
        el.wait_for(state='visible', timeout=self.timeout)
        if clear_first:
            el.fill('')
        el.fill(text)
        

    def get_element_text(self, locator: str) -> str:
        el = self.page.locator(locator)
        el.wait_for(state='visible', timeout=self.timeout)
        return el.text_content().strip()

    def wait_for_element_visible(self, locator: str):
        el = self.page.locator(locator)
        el.wait_for(state='visible', timeout=self.timeout)
        return el

    def scroll_to_element(self, locator: str):
        el = self.page.locator(locator)
        el.scroll_into_view_if_needed(timeout=self.timeout)

    def element_count(self, locator: str) -> int:
        return self.page.locator(locator).count()

    def get_attribute(self, locator: str, attribute: str) -> Union[str, None]:
        el = self.page.locator(locator)
        el.wait_for(state='visible', timeout=self.timeout)
        return el.get_attribute(attribute)

    def wait_for_text(self, locator: str, text: str):
        expect(self.page.locator(locator)).to_have_text(text, timeout=self.timeout)

    def select_option(self, locator: str, value: str):
        el = self.page.locator(locator)
        el.wait_for(state='visible', timeout=self.timeout)
        el.select_option(value)