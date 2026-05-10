"""
Purpose: Page Object Model for Cart interactions.
This site shows the cart inline on the last PDP visited (accessed via nav-cart).
Quantity is edited via <input type=number>. Fallbacks are provided for sites
that use +/- buttons or a dedicated /cart URL.
"""
from base_page import BasePage
from locators import CART, HEADER


class CartPage(BasePage):

    def goto_cart(self, base_url: str = None):
        try:
            self.click_element(CART.nav_cart)
            self._wait_for_cart()
        except Exception:
            try:
                self.click_element(CART.checkout_button)
                self._wait_for_cart()
            except Exception:
                if base_url:
                    for path in ['/cart', '/basket', '/checkout']:
                        try:
                            self.maps_to(base_url.rstrip('/') + path)
                            if self._cart_has_items():
                                return
                        except Exception:
                            continue

    def _wait_for_cart(self):
        try:
            self.page.locator(
                f'{CART.cart_items}, {CART.cart_subtotal}'
            ).first.wait_for(state='visible', timeout=self.timeout)
        except Exception:
            pass

    def _cart_has_items(self) -> bool:
        return self.page.locator(CART.cart_items).count() > 0

    def get_cart_item_count(self) -> int:
        return self.page.locator(CART.item_qty_input).count()

    def _set_quantity_direct(self, item_index: int, qty: int):
        inp = self.page.locator(CART.item_qty_input).nth(item_index)
        inp.wait_for(state='visible', timeout=self.timeout)
        inp.fill(str(qty))
        inp.dispatch_event('change')
        self.page.wait_for_timeout(500)

    def _click_qty_button(self, locator: str, item_index: int, times: int):
        btn = self.page.locator(locator).nth(item_index)
        btn.wait_for(state='visible', timeout=self.timeout)
        for _ in range(times):
            btn.click()
            self.page.wait_for_timeout(300)

    def set_item_quantity(self, item_index: int = 0, qty: int = 1):
        inp = self.page.locator(CART.item_qty_input).nth(item_index)
        if inp.count() > 0 and inp.is_visible():
            current = self._get_qty_value(item_index)
            self._set_quantity_direct(item_index, qty)
            # Verify it changed; fall back to button clicks if not
            new_val = self._get_qty_value(item_index)
            if new_val != qty:
                diff = qty - current
                if diff > 0:
                    self._click_qty_button(CART.increase_qty, item_index, diff)
                elif diff < 0:
                    self._click_qty_button(CART.decrease_qty, item_index, abs(diff))
        else:
            current = self._get_qty_value(item_index)
            diff = qty - current
            if diff > 0:
                self._click_qty_button(CART.increase_qty, item_index, diff)
            elif diff < 0:
                self._click_qty_button(CART.decrease_qty, item_index, abs(diff))

    def increase_quantity_for_item(self, item_index: int = 0, times: int = 1):
        inc = self.page.locator(CART.increase_qty)
        if inc.count() > 0 and inc.is_visible():
            self._click_qty_button(CART.increase_qty, item_index, times)
        else:
            current = self._get_qty_value(item_index)
            self._set_quantity_direct(item_index, current + times)

    def decrease_quantity_for_item(self, item_index: int = 0, times: int = 1):
        dec = self.page.locator(CART.decrease_qty)
        if dec.count() > 0 and dec.is_visible():
            self._click_qty_button(CART.decrease_qty, item_index, times)
        else:
            current = self._get_qty_value(item_index)
            self._set_quantity_direct(item_index, max(1, current - times))

    def remove_item(self, item_index: int = 0):
        remove = self.page.locator(CART.remove_item)
        if remove.count() > 0:
            remove.nth(item_index).click()
            self.page.wait_for_timeout(500)
        else:
            self._set_quantity_direct(item_index, 0)

    def _get_qty_value(self, item_index: int) -> int:
        inp = self.page.locator(CART.item_qty_input).nth(item_index)
        try:
            return int(inp.input_value())
        except Exception:
            return 1

    def get_item_quantity(self, item_index: int = 0) -> int:
        return self._get_qty_value(item_index)

    def get_item_unit_price(self, item_index: int = 0) -> float:
        el = self.page.locator(CART.item_unit_price).nth(item_index)
        return self._parse_price(el.text_content().strip())

    def get_item_total_price(self, item_index: int = 0) -> float:
        el = self.page.locator(CART.item_total).nth(item_index)
        return self._parse_price(el.text_content().strip())

    def get_cart_subtotal(self) -> float:
        try:
            txt = self.get_element_text(CART.cart_subtotal)
            return self._parse_price(txt)
        except Exception:
            return 0.0

    def proceed_to_checkout(self):
        try:
            self.click_element(CART.proceed_to_checkout)
        except Exception:
            self.click_element(CART.checkout_button)

    def _parse_price(self, price_str: str) -> float:
        import re
        match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        try:
            return float(match.group()) if match else 0.0
        except Exception:
            return 0.0
