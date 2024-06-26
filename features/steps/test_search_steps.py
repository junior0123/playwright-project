import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import expect

from features.pages.job_information_page import JobInformationPage
from features.pages.search_page import SearchPage
from features.pages.login_page import LoginPage
import os

from utils.models import JobInformation

scenarios(os.path.join(os.path.dirname(__file__), '../search_job.feature'))


@pytest.fixture(scope="function")
def search_page(page):
    return SearchPage(page)


@pytest.fixture(scope="function")
def job_information_page(page):
    return JobInformationPage(page)


@when('the user go to the LinkedIn jobs search page')
def navigate_to_search_jobs(search_page):
    search_page.go_to("https://www.linkedin.com/jobs/search/")


@when(parsers.parse('the user searches for a job title "{job_title}" in "{location}"'))
def search_for_job(search_page, job_title, location):
    search_page.search_jobs(job_title, location)


@when(parsers.parse('the user selects the filter "{mode}"'))
def select_work_mode(search_page, mode):
    search_page.select_filter(mode)


@when('the user selects single application filter')
def select_single_application(search_page):
    search_page.select_single_application()


@then('the search results should be displayed')
def verify_search_results(search_page):
    search_page.apply_filters()


@when('the user opens the filter panel')
def open_filter(search_page):
    search_page.open_filter_panel()


@then('the user navigates through all the results')
@pytest.mark.usefixtures("db_session")
def get_information(job_information_page, search_page, db_session):
    exist_next_page = True
    count = 2
    while exist_next_page:
        ids = search_page.get_links()
        for job_id in ids:
            search_page.click_on_job(job_id)
            title = job_information_page.get_job_title()
            content = job_information_page.get_job_content()
            restriction = job_information_page.location_restriction_is_present()
            url = f"https://www.linkedin.com/jobs/view/{job_id}"
            existing_post = db_session.query(JobInformation).filter_by(url=url).first()
            if existing_post is None:
                post = JobInformation(
                    job_id=job_id,
                    title=title,
                    url=url,
                    restriction=restriction,
                    state="unprocessed",
                    description=content
                )
                db_session.add(post)
                db_session.commit()
        if search_page.page_exists(count):
            search_page.click_on_next_page(count)
        else:
            exist_next_page = False
        count = count + 1
