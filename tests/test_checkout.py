from utils.actions import add_two_distinct_products, login_user, generate_user_payload, complete_checkout
from config import BASE_URL


def test_checkout_flow(page):
    # Register and login (required on this site; guest checkout sites skip this)
    payload = generate_user_payload()
    from pages.auth_page import AuthPage
    auth = AuthPage(page)
    auth.goto_register(BASE_URL)
    auth.register_user(payload)
    auth.check_registration_success()
    login_user(page, payload['email'], payload['password'], base_url=BASE_URL, navigate=False)

    add_two_distinct_products(page, base_url=BASE_URL)

    result = complete_checkout(page, payload, payment_method='Cash on Delivery', base_url=BASE_URL)

    assert result['subtotal'] > 0, f'Expected positive cart subtotal, got {result["subtotal"]}'
    assert result['confirmation'], 'Expected an order confirmation signal'
