# features/pages/login_page.py
from playwright.sync_api import Page, expect
import time


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("https://www.linkedin.com/")

    def login(self, username: str, password: str):
        self.page.pause()
        self.page.get_by_label("Email o teléfono").click()
        self.page.get_by_label("Email o teléfono").fill(username)
        self.page.get_by_label("Contraseña", exact=True).click()
        self.page.get_by_label("Contraseña", exact=True).fill(password)
        self.page.get_by_role("button", name="Inicia sesión").click()
        #time.sleep(30000)

    def verification_login_successfully(self):
        self.page.wait_for_selector('button.msg-overlay-bubble-header__control--new-convo-btn:last-child', timeout=30000)
        minimize_chat = self.page.locator('button.msg-overlay-bubble-header__control--new-convo-btn:last-child')
        minimize_chat.click()
        #expect(self.page.locator('button.msg-overlay-bubble-header__control--new-convo-btn:last-child')).to_be_hidden()

    def log_out(self):
        button = self.page.locator('img.global-nav__me-photo')
        button.click()
        logout_button = self.page.query_selector('a[href="/m/logout/"]')
        logout_button.click()
        self.page.wait_for_selector('a.nav__button-secondary', timeout= 5000)


