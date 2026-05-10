import pytest
from utils.actions import generate_user_payload, login_user
from pages.auth_page import AuthPage
from config import BASE_URL


def test_registration_login_logout(page):
    payload = generate_user_payload()
    auth = AuthPage(page)
    
    auth.goto_register(BASE_URL)
    auth.register_user(payload)
    result = auth.check_registration_success()
    assert result['success_text'] or result['redirected'], 'Expected either a success message or a redirect after registration'

    already_on_login = '/login' in auth.page.url.lower()
    login_user(page, payload['email'], payload['password'], base_url=BASE_URL, navigate=not already_on_login)
    # login_text = auth.get_login_success_text()
    # assert 'welcome' in login_text.lower() or len(login_text) > 0
    redirect_url = auth.page.url
    assert '/account' in redirect_url.lower() or '/welcome' in redirect_url.lower(), f"Unexpected redirect URL after login: {redirect_url}"

    auth.logout()
    redirect_url = auth.page.url
    assert '/login' in redirect_url.lower() or '/account' in redirect_url.lower() or redirect_url == BASE_URL, f"Unexpected redirect URL after logout: {redirect_url}"