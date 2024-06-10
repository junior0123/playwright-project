import time
from api.gemini_api import GeminiApi
from models import JobInformation
from utils.database import SessionLocal
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

user_information = dict(
    role="QA Engineer - QA Automation - QA Manual - Java Backend Developer - Python Backend Developer",
    technologies_used=["Java", "Python", "JavaScript", "Flutter", "Assembly", "Selenium", "Cypress", "Playwright",
                       "Appium", "Postman", "SQL", "Git", "Github", "Jira", "Cucumber", "Gherkin", "Jenkins",
                       "Pytest", "Junit", "TestNG"],
    skills=["GUI Testing", "API Testing", "Mobile Testing", "Web Testing", "Testing methodologies", "Bug Life Cycle",
            "Agile Methodologies"],
    years_of_experience="1 - 2 ",
    seniority="Trainee - Junior - Mid Level",
    location="Remote - Bolivia")


class AnalyzeData:
    def __init__(self, db_session):
        self.db_session = db_session
        self.api = GeminiApi()

    def get_filtered_data(self):
        return self.db_session.query(JobInformation).filter_by(restriction=False, compatible="unprocessed").all()

    def analyze_job(self, job_title, job_description):
        prompt = f"""
                Compare el perfil del usuario con la informacion del empleo.

                Información del Usuario:
                - Rol: {user_information['role']}
                - Habilidades: {', '.join(user_information['skills'])}
                - Tecnologías Utilizadas: {', '.join(user_information['technologies_used'])}
                - Años de Experiencia: {user_information['years_of_experience']} 
                - Seniority: {user_information['seniority']}
                - Ubicación: {user_information['location']}

                Información del Trabajo:
                - Título: {job_title}
                - Descripción: {job_description}
                Analiza el texto extrae la informacion de:
                    - Años de experiencia requeridos
                    - Seniority requerido
                    - Habilidades requeridas y tecnologias
                    - Ubicacion si se menciona
                Una ves hecho esto, comparalo con la informacion del usuario (SI NO CUMPLE CON EL SENIORITY O EL RANGO DE ANOS NO ENTRA CON EL DEL RANGO DEL USUARIO, DESCARTALO TOTALMENTE)
                
                SALIDA:
                - Indique el nivel de coincidencia entre el perfil del usuario y el puesto de trabajo como un porcentaje (0% a 100%), donde 100% indica una coincidencia excelente.
                """

        return self.api.generate_content(prompt)


def main():
    db_session = SessionLocal()
    try:
        analyzer = AnalyzeData(db_session)

        # Obtener los datos filtrados
        filtered_data = analyzer.get_filtered_data()
        for job in filtered_data:
            job_description = job.description
            job_title = job.title
            match_result = analyzer.analyze_job(job_title, job_description)
            print('---------------------------------***********************-------------------------------------------')
            print()
            print(f"Job Title: {job_title}, Match Result: {match_result} , url: {job.url}")
            time.sleep(4)  # sleep 4 seconds, not 4000 milliseconds

    finally:
        db_session.close()


if __name__ == "__main__":
    main()
