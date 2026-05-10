"""
Purpose: Reusable utility functions that orchestrate common flows using the page objects.
This keeps test files small and focused on assertions.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pages.auth_page import AuthPage
from pages.product_page import ProductPage
from config import BASE_URL
from locators import PLP
from typing import Dict
from faker import Faker


def generate_user_payload() -> Dict[str, str]:
    fake = Faker()
    first = fake.first_name()
    last = fake.last_name()
    email = fake.unique.safe_email()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat()
    address = fake.street_address()
    postcode = fake.postcode()
    city = fake.city()
    state = fake.state()
    country = fake.country_code(representation='alpha-2')
    phone = fake.numerify(text='##########')
    house = fake.building_number()
    return {
        'first_name': first,
        'last_name': last,
        'dob': dob,
        'address': address,
        'postcode': postcode,
        'city': city,
        'state': state,
        'country': country,
        'phone': phone,
        'email': email,
        'password': password,
        'house_number': house,
    }


def login_user(page, email: str, password: str, base_url: str = BASE_URL, navigate: bool = True):
    auth = AuthPage(page)
    if navigate:
        auth.goto_login(base_url)
    auth.login(email, password)


def add_two_distinct_products(page, base_url: str = BASE_URL):
    plp = ProductPage(page)
    for i in range(2):
        plp.maps_to(base_url)
        plp.page.locator(PLP.product_items).nth(i).wait_for(state='visible', timeout=10000)
        plp.open_product_by_index(i)
        plp.add_to_cart_from_pdp()


def complete_checkout(page, payload: Dict[str, str], payment_method: str = 'Cash on Delivery',
                      base_url: str = BASE_URL):

    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage

    cart = CartPage(page)
    cart.goto_cart(base_url)
    subtotal = cart.get_cart_subtotal()
    cart.proceed_to_checkout()

    checkout = CheckoutPage(page)
    checkout.confirm_login_step()
    checkout.fill_billing_address(payload)
    checkout.proceed_from_address()
    checkout.select_payment_method(payment_method)
    checkout.place_order()
    confirmation = checkout.get_order_confirmation()
    return {'subtotal': subtotal, 'confirmation': confirmation}