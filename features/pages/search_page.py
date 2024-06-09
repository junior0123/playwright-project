# features/pages/login_page.py
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class SearchPage:
    def __init__(self, page: Page):
        self.page = page

    def scroll_to_bottom(self, selector: str):
        self.page.evaluate(f'''
            (selector) => {{
                const scrollableElement = document.querySelector(selector);
                if (scrollableElement) {{
                    scrollableElement.scrollTop = scrollableElement.scrollHeight;
                }} else {{
                    console.log('Elemento no encontrado');
                }}
            }}
        ''', selector)
        self.page.wait_for_timeout(500)

    def scroll_element_into_view(self, selector):
        self.page.evaluate('''(selector) => {
            const element = document.querySelector(selector);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                console.log('Elemento no encontrado');
            }
        }''', selector)

    def search_jobs(self, job_title: str, location: str):
        self.page.wait_for_selector('input[aria-label="Busca por cargo, aptitud o empresa"][role="combobox"]',
                                    timeout=6000)
        job_title_input = self.page.get_by_role("combobox", name="Busca por cargo, aptitud o")
        job_title_input.click()
        job_title_input.fill(job_title)
        self.page.wait_for_selector('input[aria-label="Ciudad, provincia/estado o código postal"][role="combobox"]',
                                    timeout=6000)
        location_input = self.page.get_by_role("combobox", name="Ciudad, provincia/estado o có")
        location_input.click()
        location_input.fill(location)
        self.page.get_by_role("button", name="Buscar").click()
        expect(self.page.locator('div.jobs-search-results-list')).to_be_visible()

    def open_filter_panel(self):
        self.page.wait_for_load_state('load')
        self.page.get_by_label("Mostrar todos los filtros. Al").click()
        expect(self.page.locator('div.artdeco-modal__content')).to_be_visible()

    def publication_date(self, date: str):
        date_selectors = {
            "Cualquier momento": None,
            "Semana pasada": "Semana pasada Filtrar por «",
            "Mes pasado": "Mes pasado Filtrar por «Mes",
            "Ultimas 24 horas": "Últimas 24 horas Filtrar por"
        }
        if date not in date_selectors:
            raise ValueError(
                "Fecha de publicación no válida.")
        if date_selectors[date] is not None:
            self.page.wait_for_load_state('load')
            self.page.get_by_label("Todos los filtros", exact=True).locator("label").filter(
                has_text=date_selectors[date]).click(delay=1000)

    def select_work_mode(self, mode: str):
        work_mode_selector = {
            'Remoto': "label[for=advanced-filter-workplaceType-2]",
            'Híbrido': "label[for=advanced-filter-workplaceType-3]",
            'Presencial': "label[for=advanced-filter-workplaceType-1]"
        }
        self.scroll_element_into_view(work_mode_selector[mode])
        self.page.locator(work_mode_selector[mode]).wait_for()
        self.page.locator(work_mode_selector[mode]).click(delay=1000)

    def select_single_application(self):
        self.page.get_by_text("Desactivado Activar/desactivar el filtro Solicitud sencilla").click()

    def apply_filters(self):
        self.page.wait_for_load_state('load')
        self.page.locator('button[data-test-reusables-filters-modal-show-results-button="true"]').wait_for(state='visible')
        # self.page.wait_for_selector('button[aria-label="Aplicar los filtros actuales para mostrar resultados"]',
        #                             timeout=5000)
        self.page.locator('button[data-test-reusables-filters-modal-show-results-button="true"]').click()
        #self.page.get_by_label("Aplicar los filtros actuales").click(delay=1000)
        self.page.wait_for_selector('button[aria-label="Restablecer filtros aplicados"]', timeout=1200000)
        expect(self.page.get_by_label("Restablecer filtros aplicados")).to_be_visible()
        self.page.wait_for_load_state('load')
        expect(self.page.locator('ul.scaffold-layout__list-container')).to_be_visible()

    def go_to(self, url):
        self.page.goto(url)
        expect(self.page.locator('ul.scaffold-layout__list-container')).to_be_visible()

    def get_links(self):
        self.scroll_to_bottom('div.jobs-search-results-list')
        enlaces = self.page.query_selector_all('li.jobs-search-results__list-item')
        ids = [enlace.get_attribute("data-occludable-job-id") for enlace in enlaces]
        return ids

    def click_on_job(self, job_id):

        self.page.wait_for_load_state('load')
        expect(self.page.locator('ul.scaffold-layout__list-container')).to_be_visible()
        element_selector = f'[data-occludable-job-id="{job_id}"]'
        self.scroll_element_into_view(element_selector)
        self.page.click(element_selector)
        self.scroll_to_bottom('div.jobs-search__job-details--wrapper')
        self.page.wait_for_load_state('load')

    def click_on_next_page(self, page_number):
        id_page_selector = f'li[data-test-pagination-page-btn="{page_number}"] button'
        self.page.wait_for_selector(id_page_selector, timeout=3000)
        self.page.click(id_page_selector)

    def page_exists(self, page_number):

        id_page_selector = f'li[data-test-pagination-page-btn="{page_number}"] button'
        try:
            locator = self.page.locator(id_page_selector)
            locator.wait_for(timeout=3000)
            return True
        except PlaywrightTimeoutError:
            return False
