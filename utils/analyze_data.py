import time
from api.gemini_api import GeminiApi
from .models import JobInformation
from utils.database import SessionLocal
from dotenv import load_dotenv
import re
from tqdm import tqdm
from config.settings import Settings

load_dotenv()


class AnalyzeData:
    def __init__(self, db_session):
        self.db_session = db_session
        self.api = GeminiApi()

    def get_filtered_data(self):
        return self.db_session.query(JobInformation).filter_by(restriction=False, state="unprocessed").all()

    def analyze_job(self, job_title, job_description):
        user_information = Settings.USER_INFORMATION
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

    def extract_percentage(self, text):
        matches = re.findall(r'(\d+)%', text)
        if matches:
            return int(matches[-1])
        else:
            return None


def main():
    db_session = SessionLocal()
    try:
        analyzer = AnalyzeData(db_session)
        filtered_data = analyzer.get_filtered_data()
        job_matches = []
        for job in tqdm(filtered_data, desc="Processing"):
            job_description = job.description
            job_title = job.title
            match_result = analyzer.analyze_job(job_title, job_description)
            percentage = analyzer.extract_percentage(match_result)
            if percentage is not None:
                job.match_percentage = percentage
                job_matches.append((job_title, job.url, percentage))
            job.ai_analysis = match_result
            job.state = "processed"
            db_session.commit()
            time.sleep(1)  #To not exceed 15 requests per minute
        job_matches.sort(key=lambda x: x[2], reverse=True)
        index = 0
        for title, url, percentage in job_matches:
            print(f" {index}. {title}, URL: {url}, Match Percentage: {percentage}%")
            index += 1
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
