# features/pages/login_page.py
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re

class JobInformationPage:
    def __init__(self, page: Page):
        self.page = page

    def get_job_title(self):
        self.page.wait_for_load_state('load')
        expect(self.page.locator('div.t-24.job-details-jobs-unified-top-card__job-title h1 a')).to_be_visible(timeout=3000)
        locator = self.page.locator('div.t-24.job-details-jobs-unified-top-card__job-title h1 a')
        locator.wait_for(timeout=5000, state='visible')

        title_locator = 'div.t-24.job-details-jobs-unified-top-card__job-title h1 a'
        self.page.wait_for_selector(title_locator, timeout=60000)
        title_element = self.page.query_selector(title_locator)
        title = title_element.inner_text()
        return title

    def get_job_content(self):
        self.page.wait_for_load_state('load')
        job_content_locator = '#job-details'
        expect(self.page.locator(job_content_locator)).to_be_visible(timeout=3000)
        self.page.wait_for_selector(job_content_locator, timeout=30000)
        job_description = self.page.inner_text(job_content_locator)
        cleaned_description = re.sub(r'\n+', '\n', job_description).strip()
        return cleaned_description

    def location_restriction_is_present(self):
        try:
            locator = self.page.locator('h2.fit-content-width.text-body-medium')
            locator.wait_for(timeout=2000)
        except PlaywrightTimeoutError:
            return False

        if locator.count() > 0:
            h2_element = locator.first
            location_restriction_text = h2_element.text_content()
            if "Tu ubicación no coincide con los requisitos del país." in location_restriction_text:
                return True

        return False

