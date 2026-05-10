"""
Purpose: Page Object Model for the multi-step Checkout flow.
This site has 4 steps: cart review → sign-in confirm → address → payment.
Each step has a fallback for sites that use a single-page or different step structure.
"""
from base_page import BasePage
from locators import CHECKOUT
from typing import Dict


class CheckoutPage(BasePage):

    def confirm_login_step(self):
        btn = self.page.locator(CHECKOUT.proceed_2)
        try:
            btn.wait_for(state='visible', timeout=5000)
            btn.click()
            self.page.wait_for_timeout(500)
        except Exception:
            pass

    def fill_billing_address(self, payload: Dict[str, str]):
        fields = [
            (CHECKOUT.billing_country,      payload.get('country', ''),      'select'),
            (CHECKOUT.billing_postcode,     payload.get('postcode', ''),     'input'),
            (CHECKOUT.billing_house_number, payload.get('house_number', ''), 'input'),
            (CHECKOUT.billing_address,      payload.get('address', ''),      'input'),
            (CHECKOUT.billing_city,         payload.get('city', ''),         'input'),
            (CHECKOUT.billing_state,        payload.get('state', ''),        'input'),
        ]
        for locator, value, field_type in fields:
            if not value:
                continue
            try:
                el = self.page.locator(locator)
                el.wait_for(state='visible', timeout=5000)
                if field_type == 'select':
                    el.select_option(value)
                else:
                    el.fill(value)
                self.page.wait_for_timeout(200)
            except Exception:
                pass

    def proceed_from_address(self):
        btn = self.page.locator(CHECKOUT.proceed_3)
        try:
            btn.wait_for(state='visible', timeout=self.timeout)
            for _ in range(25):
                if btn.is_enabled():
                    break
                self.page.wait_for_timeout(200)
            btn.click()
            self.page.wait_for_timeout(500)
        except Exception:
            for sel in ["button[type='submit']", "button:has-text('Proceed')",
                        "button:has-text('Continue')", "button:has-text('Next')"]:
                try:
                    fb = self.page.locator(sel).first
                    if fb.is_visible() and fb.is_enabled():
                        fb.click()
                        return
                except Exception:
                    continue

    def select_payment_method(self, method: str = 'Cash on Delivery'):
        sel = self.page.locator(CHECKOUT.payment_method)
        try:
            sel.wait_for(state='visible', timeout=self.timeout)
            try:
                sel.select_option(label=method)
                return
            except Exception:
                pass

            try:
                sel.select_option(method.lower().replace(' ', '-'))
                return
            except Exception:
                pass
        except Exception:
            pass
        #
        for sel_str in [
            f"input[type='radio'][value*='{method}']",
            f"label:has-text('{method}')",
            f"[data-test*='payment']:has-text('{method}')",
        ]:
            try:
                el = self.page.locator(sel_str).first
                if el.count() > 0:
                    el.click()
                    return
            except Exception:
                continue

    def place_order(self):

        try:
            self.click_element(CHECKOUT.place_order)
        except Exception:
            for sel in ["button:has-text('Confirm')", "button:has-text('Place Order')",
                        "button:has-text('Submit')", "button[type='submit']"]:
                try:
                    btn = self.page.locator(sel).first
                    if btn.is_visible() and btn.is_enabled():
                        btn.click()
                        return
                except Exception:
                    continue

    def get_order_confirmation(self) -> str:
        try:
            el = self.page.locator(CHECKOUT.order_confirmation).first
            el.wait_for(state='visible', timeout=15000)
            return el.text_content().strip()
        except Exception:
            return self.page.url

    def get_checkout_total(self) -> float:
        from locators import CART
        try:
            txt = self.get_element_text(CART.cart_subtotal)
            return self._parse_price(txt)
        except Exception:
            return 0.0

    def _parse_price(self, price_str: str) -> float:
        import re
        match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        try:
            return float(match.group()) if match else 0.0
        except Exception:
            return 0.0
