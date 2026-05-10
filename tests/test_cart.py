from utils.actions import add_two_distinct_products, login_user, generate_user_payload
from pages.cart_page import CartPage
from config import BASE_URL


def test_cart_manipulation_and_totals(page):
    # Login so cart persists (required on this site; harmless on sites that allow guest cart)
    payload = generate_user_payload()
    from pages.auth_page import AuthPage
    auth = AuthPage(page)
    auth.goto_register(BASE_URL)
    auth.register_user(payload)
    auth.check_registration_success()
    login_user(page, payload['email'], payload['password'], base_url=BASE_URL, navigate=False)

    add_two_distinct_products(page, base_url=BASE_URL)

    cart = CartPage(page)
    cart.goto_cart(BASE_URL)

    assert cart.get_cart_item_count() >= 2, 'Expected at least 2 items in cart'

    cart.set_item_quantity(0, 3)
    assert cart.get_item_quantity(0) == 3, f'Expected qty 3, got {cart.get_item_quantity(0)}'

    cart.set_item_quantity(0, 2)
    assert cart.get_item_quantity(0) == 2, f'Expected qty 2, got {cart.get_item_quantity(0)}'

    unit_price = cart.get_item_unit_price(0)
    qty = cart.get_item_quantity(0)
    line_total = cart.get_item_total_price(0)
    assert unit_price > 0, 'Expected positive unit price'
    assert abs(unit_price * qty - line_total) < 0.02, (
        f'Price maths off: {unit_price} × {qty} ≠ {line_total}'
    )

    subtotal = cart.get_cart_subtotal()
    assert subtotal > 0, f'Expected positive subtotal, got {subtotal}'
