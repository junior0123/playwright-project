# conftest.py
import os

import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from pytest_bdd import given, then, when
from utils.db_fixture import db_session
from features.pages.login_page import LoginPage
from utils.database import engine, Base

load_dotenv()


@pytest.fixture(scope="session")
def playwright_context():
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=['--start-maximized'], headless=False, slow_mo=100)
            context = browser.new_context(no_viewport=True)  #browser window
            context.clear_cookies()
            yield context  #proporciona el contexto para otros test
            context.close()
            browser.close()
    except Exception as e:
        print(f"Error: {e}")


@pytest.fixture(scope="function")
def page(playwright_context):
    try:
        page = playwright_context.new_page()  #tab window
        yield page  #proporciona la pagina a las funciones que lo necesiten
        page.close()
    except Exception as e:
        print(f"Error: {e}")


@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Limpia la base de datos después de los tests
    #Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)


@given('the user is on the login page')
def navigate_to_login_page(login_page):
    login_page.navigate()


@when('the user logs in with valid credentials')
def login_with_valid_credentials(login_page):
    username = os.getenv('APP_USERNAME')
    password = os.getenv('APP_PASSWORD')
    login_page.login(username, password)


@then('the user should be redirected to the dashboard')
def verify_dashboard_redirect(login_page):
    login_page.verification_login_successfully()


@then('the user logout')
def logout_from_the_site(login_page):
    login_page.log_out()
