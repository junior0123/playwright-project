# features/pages/login_page.py
from playwright.sync_api import Page, expect


class SearchPage:
    def __init__(self, page: Page):
        self.page = page

    def search_jobs(self, job_title: str, location: str):
        self.page.get_by_role("combobox", name="Busca por cargo, aptitud o").fill(job_title)
        self.page.get_by_role("combobox", name="Ciudad, provincia/estado o có").fill(location)
        self.page.get_by_role("button", name="Buscar").click()
        expect(self.page.locator('div.jobs-search-results-list')).to_be_visible()

    def open_filter_panel(self):
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
                "Fecha de publicación no válida. Use 'Cualquier momento', 'Semana pasada', 'Mes pasado' o 'Ultimas 24 horas'.")
        if date_selectors[date] is not None:
            self.page.get_by_label("Todos los filtros", exact=True).locator("label").filter(
                has_text=date_selectors[date]).click()

    def select_work_mode(self, mode: str):
        if mode not in ['Remoto', 'Híbrido', 'Presencial']:
            raise ValueError("El modo de trabajo debe ser 'Remoto', 'Híbrido', o 'Presencial'.")
        work_mode_selector = {
            'Remoto': "En remoto Filtrar por «En",
            'Híbrido': "Híbrido Filtrar por «Híbrido»",
            'Presencial': "Presencial Filtrar por «"
        }
        # Hacer clic en el filtro correspondiente
        self.page.get_by_label("Todos los filtros", exact=True).locator("label").filter(
            has_text=work_mode_selector[mode]).click()
    def select_single_application(self):
        self.page.get_by_text("Desactivado Activar/desactivar el filtro Solicitud sencilla").click()

    def apply_filters(self):
        self.page.get_by_label("Aplicar los filtros actuales").click()
        expect(self.page.get_by_label("Restablecer filtros aplicados")).to_be_visible()

    def go_to(self, url):
        self.page.goto(url)
        #self.page.wait_for_load_state('networkidle')
        expect(self.page.locator('ul.scaffold-layout__list-container')).to_be_visible()
