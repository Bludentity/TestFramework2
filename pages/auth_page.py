"""
pages/auth_page.py
Purpose: Page Object Model for authentication-related pages (Registration & Login).
All methods use BasePage abstractions and locators from locators.py to avoid raw selectors
in tests. This class encapsulates flows like register, login and logout.
"""
from base_page import BasePage
from locators import AUTH, HEADER
from typing import Dict


class AuthPage(BasePage):
    def goto_register(self, base_url: str):
        self.maps_to(base_url)
        self.click_element(AUTH.login_link)
        self.click_element(AUTH.register_link)

    def register_user(self, payload: Dict[str, str]):
        self.input_text(AUTH.reg_first_name, payload.get('first_name', ''))
        self.input_text(AUTH.reg_last_name, payload.get('last_name', ''))

        try:
            self.input_text(AUTH.reg_dob, payload.get('dob', ''))
        except Exception:
            pass

        
        country_selected = False
        try:
            self.select_option(AUTH.reg_country, payload.get('country', ''))
            country_selected = True
        except Exception:
            try:
                self.input_text(AUTH.reg_country, payload.get('country', ''))
            except Exception:
                pass

        self.input_text(AUTH.reg_postcode, payload.get('postcode', ''))

        try:
            self.input_text(AUTH.reg_house_number, payload.get('house_number', ''))
        except Exception:
            pass

        if country_selected:
            try:
                self.page.locator(AUTH.reg_address).wait_for(state='visible', timeout=5000)
            except Exception:
                pass

        try:
            if not self.page.locator(AUTH.reg_address).input_value():
                self.input_text(AUTH.reg_address, payload.get('address', ''))
        except Exception:
            try:
                self.input_text(AUTH.reg_address, payload.get('address', ''))
            except Exception:
                pass

        try:
            if not self.page.locator(AUTH.reg_city).input_value():
                self.input_text(AUTH.reg_city, payload.get('city', ''))
        except Exception:
            try:
                self.input_text(AUTH.reg_city, payload.get('city', ''))
            except Exception:
                pass

        try:
            if not self.page.locator(AUTH.reg_state).input_value():
                self.input_text(AUTH.reg_state, payload.get('state', ''))
        except Exception:
            try:
                self.select_option(AUTH.reg_state, payload.get('state', ''))
            except Exception:
                pass

        self.input_text(AUTH.reg_phone, payload.get('phone', ''))
        self.input_text(AUTH.reg_email, payload.get('email', ''))
        self.input_text(AUTH.reg_password, payload.get('password', ''))

        try:
            self.input_text(AUTH.reg_password_confirm, payload.get('password', ''))
        except Exception:
            pass

        self.click_element(AUTH.reg_submit)

    def get_registration_success_text(self) -> str:
        return self.get_element_text(AUTH.reg_success_text)
    
    def check_registration_success(self, timeout: int = 15000) -> dict:
        success_text = ''
        try:
            self.page.locator(AUTH.reg_success_text).wait_for(state='visible', timeout=timeout)
            success_text = self.page.locator(AUTH.reg_success_text).text_content().strip()
        except Exception:
            pass
        try:
            self.page.wait_for_url(lambda url: '/register' not in url, timeout=timeout)
            return {'success_text': success_text, 'redirected': True}
        except Exception:
            return {'success_text': success_text, 'redirected': False}

    def goto_login(self, base_url: str):
        self.maps_to(base_url)
        self.click_element(AUTH.login_link)

    def login(self, email: str, password: str):
        self.input_text(AUTH.login_email, email)
        self.input_text(AUTH.login_password, password)
        with self.page.expect_navigation(wait_until='load', timeout=15000):
            self.click_element(AUTH.login_submit)

    def get_login_success_text(self) -> str:
        return self.get_element_text(AUTH.login_success_text)

    def logout(self):
        try:
            with self.page.expect_navigation(wait_until='load', timeout=15000):
                self.click_element(HEADER.logout_link)
        except Exception:
            self.click_element(HEADER.menu_button)
            with self.page.expect_navigation(wait_until='load', timeout=15000):
                self.click_element(HEADER.logout_link)
