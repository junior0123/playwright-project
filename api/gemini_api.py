import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import os

load_dotenv()


class GeminiApi:

    def __init__(self):
        self.API_KEY = os.getenv("API_KEY")
        genai.configure(api_key=self.API_KEY)
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash-001', safety_settings=self.safety_settings)

    def generate_content(self, prompt: str):
        response = self.model.generate_content(prompt)
        #print(response.text)
        return response.text


def main():
    api = GeminiApi()
    prompt = "Escribe un poema sobre el amor."
    api.generate_content(prompt)


if __name__ == "__main__":
    main()
