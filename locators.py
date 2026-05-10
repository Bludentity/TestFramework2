"""
Purpose: Centralized locator repository. All CSS/XPath selectors used by pages and tests
should be defined here. Grouped logically for easy replacement when targeting different sites.

Structure: A top-level dictionary-like class with attributes for groups: Auth, Header,
ProductList, ProductDetail, Cart, Checkout.
"""
from dataclasses import dataclass


@dataclass
class Auth:
    # Registration
    register_link: str = "a[href*='/auth/register']"
    reg_first_name: str = "[data-test='first-name']"
    reg_last_name: str = "[data-test='last-name']"
    reg_dob: str = "[data-test='dob']"
    reg_address: str = "[data-test='street']"
    reg_house_number: str = "[data-test='house_number']"
    reg_postcode: str = "[data-test='postal_code']"
    reg_city: str = "[data-test='city']"
    reg_state: str = "[data-test='state']"
    reg_country: str = "[data-test='country']"
    reg_phone: str = "[data-test='phone']"
    reg_email: str = "[data-test='email']"
    reg_password: str = "[data-test='password']"
    reg_password_confirm: str = "[data-test='password-confirm']"
    reg_submit: str = "[data-test='register-submit']"
    reg_success_text: str = "div.alert-success"

    # Login
    login_link: str = "a[href*='/auth/login']"
    login_email: str = "[data-test='email']"
    login_password: str = "[data-test='password']"
    login_submit: str = "[data-test='login-submit']"
    login_success_text: str = "div.account-header"


@dataclass
class Header:
    # Prefer data-test attributes when possible
    search_input: str = "[data-test='search-query']"
    search_button: str = "[data-test='search-submit']"
    menu_button: str = "[data-test='nav-menu']"
    cart_link: str = "a[href*='cart']"
    logout_link: str = "a[data-test='nav-sign-out']"


@dataclass
class ProductList:
    # PLP selectors
    product_items: str = "a.card"
    product_no_results: str = "[data-test='no-results']"
    product_price: str = "[data-test='product-price']"
    product_title: str = "[data-test='product-name']"
    category_filter: str = "select#category"
    price_min: str = "input#price_min"
    price_max: str = "input#price_max"
    apply_filter: str = "button.apply-filter"
    price_slider_min: str = ".ngx-slider-pointer-min"
    price_slider_max: str = ".ngx-slider-pointer-max"
    price_slider_bar: str = ".ngx-slider-span.ngx-slider-bar-wrapper"
    add_to_cart_button: str = "[data-test='add-to-cart']"


@dataclass
class ProductDetail:
    product_name: str = "[data-test='product-name']"
    product_price: str = "[data-test='unit-price']"
    product_description: str = "[data-test='product-description']"
    qty_input: str = "[data-test='quantity']"
    increase_qty: str = "[data-test='increase-quantity']"
    decrease_qty: str = "[data-test='decrease-quantity']"
    add_to_cart: str = "[data-test='add-to-cart']"
    add_success_modal: str = "[data-test='add-success-modal']"


@dataclass
class Cart:
    nav_cart: str = "[data-test='nav-cart']"
    cart_quantity_badge: str = "[data-test='cart-quantity']"
    # Cart item row — each row contains title, qty input, unit price, line price
    cart_items: str = "[data-test='product-title']"
    item_name: str = "[data-test='product-title']"
    item_qty_input: str = "[data-test='product-quantity']"
    item_unit_price: str = "[data-test='product-price']"
    item_total: str = "[data-test='line-price']"

    increase_qty: str = "[data-test='increase-qty']"   # fallback for sites with buttons
    decrease_qty: str = "[data-test='decrease-qty']"   # fallback for sites with buttons
    remove_item: str = "[data-test='remove-item']"      # fallback for sites with remove btn
    cart_subtotal: str = "[data-test='cart-total']"
    proceed_to_checkout: str = "[data-test='proceed-1']"
    checkout_button: str = "a[href*='checkout']"        # fallback href-based nav


@dataclass
class Checkout:
    # Sign-in confirmation (some sites skip this)
    proceed_2: str = "[data-test='proceed-2']"
    # Shipping address
    billing_country: str = "[data-test='country']"
    billing_postcode: str = "[data-test='postal_code']"
    billing_house_number: str = "[data-test='house_number']"
    billing_address: str = "[data-test='street']"
    billing_city: str = "[data-test='city']"
    billing_state: str = "[data-test='state']"
    proceed_3: str = "[data-test='proceed-3']"
    # Payment
    payment_method: str = "[data-test='payment-method']"
    place_order: str = "[data-test='finish']"
    # Confirmation
    order_confirmation: str = "[data-test='order-confirmation'], .order-confirmation, h2.confirmation"


AUTH = Auth()
HEADER = Header()
PLP = ProductList()
PDP = ProductDetail()
CART = Cart()
CHECKOUT = Checkout()
