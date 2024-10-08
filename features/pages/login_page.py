
from playwright.sync_api import Page, expect
import time


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto("https://www.linkedin.com/login/es")
        #self.page.pause()

    def login(self, username: str, password: str):
        self.page.get_by_label("Email o teléfono").click()
        self.page.get_by_label("Email o teléfono").fill(username)
        self.page.get_by_label("Contraseña", exact=True).click()
        self.page.get_by_label("Contraseña", exact=True).fill(password)
        self.page.get_by_label("Iniciar sesión", exact=True).click()

    def verification_login_successfully(self):

        self.page.wait_for_selector('button.msg-overlay-bubble-header__control--new-convo-btn', timeout=240000)
        self.page.wait_for_load_state('load')
        buttons = self.page.locator('button.msg-overlay-bubble-header__control--new-convo-btn')
        minimize_chat = buttons.nth(-1)
        minimize_chat.click(delay=500)

    def log_out(self):
        button = self.page.locator('img.global-nav__me-photo')
        button.click()
        self.page.wait_for_load_state('load')
        self.page.wait_for_selector('a[href="/m/logout/"]', timeout=30000)
        logout_button = self.page.query_selector('a[href="/m/logout/"]')
        logout_button.click()
        self.page.wait_for_selector('a.nav__button-secondary', timeout=120000)
