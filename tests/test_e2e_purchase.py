"""
End-to-end purchase flow: register → login → search → PDP → add to cart → checkout.
"""
import pytest
from config import BASE_URL
from utils.actions import generate_user_payload, login_user, add_two_distinct_products, complete_checkout
from pages.auth_page import AuthPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


def test_e2e_purchase_flow(page):
    # 1. Register
    payload = generate_user_payload()
    auth = AuthPage(page)
    auth.goto_register(BASE_URL)
    auth.register_user(payload)
    result = auth.check_registration_success()
    assert result['success_text'] or result['redirected'], 'Registration did not succeed'

    # 2. Login immediately after registration redirect
    login_user(page, payload['email'], payload['password'], base_url=BASE_URL, navigate=False)
    assert '/account' in auth.page.url.lower() or '/welcome' in auth.page.url.lower(), (
        f'Unexpected URL after login: {auth.page.url}'
    )

    # 3. Search and validate PLP results
    plp = ProductPage(page)
    plp.maps_to(BASE_URL)
    plp.search('hammer')
    count = plp.get_products_count()
    assert count > 0, 'Expected search results for "hammer"'

    # 4. Open first PDP and validate fields
    plp.open_product_by_index(0)
    name = plp.get_pdp_name()
    price = float(plp.get_pdp_price())
    desc = plp.get_pdp_description()
    assert name, 'PDP name should not be empty'
    assert price > 0, f'PDP price should be positive, got {price}'
    assert desc, 'PDP description should not be empty'

    # 5. Add two distinct products to cart
    add_two_distinct_products(page, base_url=BASE_URL)

    # 6. Validate cart
    cart = CartPage(page)
    cart.goto_cart(BASE_URL)
    assert cart.get_cart_item_count() >= 2, 'Expected at least 2 items in cart'
    subtotal = cart.get_cart_subtotal()
    assert subtotal > 0, f'Expected positive cart subtotal, got {subtotal}'

    # 7. Complete checkout
    result = complete_checkout(page, payload, payment_method='Cash on Delivery', base_url=BASE_URL)
    assert result['confirmation'], 'Expected an order confirmation signal after checkout'
