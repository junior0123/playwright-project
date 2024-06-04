import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import expect
from features.pages.home_page import HomePage
from features.pages.search_page import SearchPage
from features.pages.login_page import LoginPage
import os

scenarios(os.path.join(os.path.dirname(__file__), '../search_job.feature'))
@pytest.fixture(scope="function")
def search_page(page):
    return SearchPage(page)

@pytest.fixture(scope="function")
def home_page(page):
    return HomePage(page)

@when('the user go to the LinkedIn jobs search page')
def navigate_to_search_jobs(search_page):
    
    search_page.go_to("https://www.linkedin.com/jobs/search/")



@when(parsers.parse('the user searches for a job title "{job_title}" in "{location}"'))
def search_for_job(search_page, job_title, location):
    search_page.search_jobs(job_title, location)
    
@when(parsers.parse('the user selects the work mode "{mode}"'))
def select_work_mode(search_page, mode):
    search_page.select_work_mode(mode)

@when(parsers.parse('the user selects the "{date}" date'))
def select_publication_date(search_page, date):  # Nombre más descriptivo
    search_page.publication_date(date)

@when('the user selects single application filter')
def select_single_application(search_page):
    search_page.select_single_application()


@then('the search results should be displayed')
def verify_search_results(search_page):
    search_page.apply_filters()

@when('the user opens the filter panel')
def step_when(search_page):
    search_page.open_filter_panel()
