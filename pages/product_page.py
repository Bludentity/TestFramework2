"""
Purpose: Page Object Model for product listing (PLP) and product detail (PDP) interactions.
Contains methods to search, filter, navigate to PDP, and add products to cart.
"""
from base_page import BasePage
from locators import HEADER, PLP, PDP
from typing import Dict


class ProductPage(BasePage):
    def search(self, query: str):
        try:
            self.page.locator(PLP.product_items).first.wait_for(state='attached', timeout=self.timeout)
        except Exception:
            pass
        self.input_text(HEADER.search_input, query)
        self.click_element(HEADER.search_button)

        try:
            self.page.wait_for_function(
                """(args) => {
                    const [itemSel, titleSel, noResSel, query] = args;
                    const noRes = document.querySelector(noResSel);
                    if (noRes && noRes.offsetParent !== null) return true;
                    const first = document.querySelector(itemSel);
                    if (!first) return false;
                    // Try the configured title selector first, then any text-bearing child
                    const name = first.querySelector(titleSel) || first.querySelector('h1,h2,h3,h4,a,span');
                    return name && name.textContent.toLowerCase().includes(query.toLowerCase());
                }""",
                arg=[PLP.product_items, PLP.product_title, PLP.product_no_results, query],
                timeout=15000
            )
        except Exception:
            try:
                self.page.locator(f'{PLP.product_no_results}, {PLP.product_items}').first.wait_for(
                    state='visible', timeout=10000
                )
            except Exception:
                pass

    def get_no_results_text(self) -> str:
        el = self.page.locator(PLP.product_no_results)
        return el.text_content().strip() if el.count() > 0 else ''

    def apply_category_filter(self, category_value: str):
        self.page.select_option(PLP.category_filter, category_value)
        if self.page.locator(PLP.apply_filter).is_visible():
            self.click_element(PLP.apply_filter)

    def apply_price_filter(self, min_price=None, max_price=None) -> dict:
        try:
            self.page.locator(PLP.price_slider_max).wait_for(state='visible', timeout=self.timeout)
        except Exception:
            pass
        min_handle = self.page.locator(PLP.price_slider_min)
        max_handle = self.page.locator(PLP.price_slider_max)

        if max_handle.count() > 0:
            range_min = float(max_handle.get_attribute('aria-valuemin') or 0)
            range_max = float(max_handle.get_attribute('aria-valuemax') or 200)
            bar = self.page.locator(PLP.price_slider_bar).first
            bar_width = bar.bounding_box()['width']
            pixels_per_unit = bar_width / (range_max - range_min)

            def _drag_handle(handle, target_value: float) -> float:
                current_value = float(handle.get_attribute('aria-valuenow') or 0)
                delta_px = (target_value - current_value) * pixels_per_unit
                box = handle.bounding_box()
                cx = box['x'] + box['width'] / 2
                cy = box['y'] + box['height'] / 2
                self.page.mouse.move(cx, cy)
                self.page.mouse.down()
                self.page.mouse.move(cx + delta_px, cy, steps=20)
                self.page.mouse.up()
                
                for _ in range(3):
                    landed = float(handle.get_attribute('aria-valuenow') or 0)
                    error = target_value - landed
                    if abs(error) < 1:
                        break
                    nudge_px = error * pixels_per_unit
                    box = handle.bounding_box()
                    cx = box['x'] + box['width'] / 2
                    cy = box['y'] + box['height'] / 2
                    self.page.mouse.move(cx, cy)
                    self.page.mouse.down()
                    self.page.mouse.move(cx + nudge_px, cy, steps=5)
                    self.page.mouse.up()
                landed = float(handle.get_attribute('aria-valuenow') or 0)
                assert abs(landed - target_value) < abs(current_value - target_value), (
                    f'Slider did not move toward target {target_value}: '
                    f'started at {current_value}, landed at {landed}'
                )
                return landed

            snapped_min = _drag_handle(min_handle, float(min_price)) if min_price is not None and min_handle.count() > 0 else None
            snapped_max = _drag_handle(max_handle, float(max_price)) if max_price is not None else None

            prev = None
            for _ in range(15):
                self.page.wait_for_timeout(300)
                current = self.page.locator(PLP.product_items).count()
                if current == prev:
                    break
                prev = current
            return {'min': snapped_min, 'max': snapped_max}
        else:
            if min_price:
                self.input_text(PLP.price_min, str(min_price))
            if max_price:
                self.input_text(PLP.price_max, str(max_price))
            if self.page.locator(PLP.apply_filter).is_visible():
                self.click_element(PLP.apply_filter)
            return {'min': float(min_price) if min_price is not None else None,
                    'max': float(max_price) if max_price is not None else None}
       

    def get_price_filter_values(self) -> dict:
        min_handle = self.page.locator(PLP.price_slider_min)
        max_handle = self.page.locator(PLP.price_slider_max)
        return {
            'min': float(min_handle.get_attribute('aria-valuenow')) if min_handle.count() > 0 else None,
            'max': float(max_handle.get_attribute('aria-valuenow')) if max_handle.count() > 0 else None,
        }
        

    def get_products_count(self) -> int:
        prev_count = None
        for _ in range(10):
            current_count = self.page.locator(PLP.product_items).count()
            if current_count == prev_count:
                break
            prev_count = current_count
            self.page.wait_for_timeout(300)
        return prev_count or 0
    

    def get_product_names(self) -> list:
        return self.page.locator(PLP.product_title).all_inner_texts()

    def get_product_prices(self) -> list:
        prev_count = -1
        for _ in range(10):
            current_count = self.page.locator(PLP.product_price).count()
            if current_count == prev_count:
                break
            prev_count = current_count
            self.page.wait_for_timeout(500)
        
        els = self.page.locator(PLP.product_price).all()
        prices = []
        for el in els:
            try:
                text = el.text_content().strip().replace('$', '').replace(',', '')
                prices.append(float(text))
            except (ValueError, TypeError):
                pass
        return prices

    def open_product_by_index(self, index: int = 0):
        items = self.page.locator(PLP.product_items)
        items.nth(index).wait_for(state='visible', timeout=self.timeout)
        try:
            items.nth(index).locator(PLP.product_title).click()
        except Exception:
            items.nth(index).click()
        self.page.wait_for_load_state('load')

    def add_first_n_products_to_cart(self, n: int = 1):
        items = self.page.locator(PLP.product_items)
        count = items.count()
        for i in range(min(n, count)):
            items.nth(i).locator(PLP.add_to_cart_button).click()

    def get_pdp_name(self) -> str:
        return self.get_element_text(PDP.product_name)

    def get_pdp_price(self) -> str:
        return self.get_element_text(PDP.product_price)

    def get_pdp_description(self) -> str:
        return self.get_element_text(PDP.product_description)

    def add_to_cart_from_pdp(self, quantity: int = 1):
        try:
            self.input_text(PDP.qty_input, str(quantity))
        except Exception:
            pass
        # Record badge count before clicking so we can detect the increment
        badge = self.page.locator("[data-test='cart-quantity'], .cart-count, .cart-badge")
        before = 0
        try:
            before = int(badge.first.text_content().strip())
        except Exception:
            pass
        self.click_element(PDP.add_to_cart)
        # Wait for cart badge to increment, or success modal, or a fixed fallback
        try:
            self.page.wait_for_function(
                """(args) => {
                    const [sels, before] = args;
                    for (const sel of sels) {
                        const el = document.querySelector(sel);
                        if (el && parseInt(el.textContent.trim() || '0') > before) return true;
                    }
                    return false;
                }""",
                arg=[["[data-test='cart-quantity']", ".cart-count", ".cart-badge"], before],
                timeout=8000
            )
        except Exception:
            try:
                self.page.locator(PDP.add_success_modal).wait_for(state='visible', timeout=3000)
            except Exception:
                self.page.wait_for_timeout(1500)
