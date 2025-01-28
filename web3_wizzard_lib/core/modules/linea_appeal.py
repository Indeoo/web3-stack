import webbrowser

from loguru import logger
from sybil_engine.module.module import Module
import requests


class LineaAppeal(Module):
    module_name = 'LINEA_APPEAL'
    module_config = None

    # with open("resources/linea_appeal.txt") as f:
    #     linea_appeal_reason = f.read()

    linea_appeal_reason = """
        Меня проект Linea забанили акки и пометили как сибила. Планирую писать апелляции с указанием причин почему я не сибил. 
        Вот список аргументов: 
        1. Получал дроп LayerZero. 
        2. Получал дроп ZKsync 
        3. Получал дроп ODOS 
        4. Был активен в более чем 10 сетях 
        5. Потратил 60-100$ на кампании Линея начиная от Defi Voyage 
        6. Прошел POH 
        7. Получил дроп Scroll 
        8. Обьем торгов по аккаунту более 100 тыс$. Возьми составь аргументации для 10 аккаунтов, 
        выбрав рандомно от 5 до 8 из этих причин для разбана. Все на англ.
        """

    def execute(self, account, chain="LINEA", statistic_write="GOOGLE"):
        base_url = "https://docs.google.com/forms/d/e/1FAIpQLSfkbHzC1hZTy6u5R8S5i6wQ2xCyUZQjvucmlyChwg04fJIO5Q/viewform"

        reason = self.get_reason()

        logger.info(reason)

        payload = {
            "entry.1292139045": account.address,
            "entry.1099559693": "",
            "entry.1296389817": reason['choices'][0]['message']['content']
            # Add other entries based on the form's structure
        }

        # Build the pre-filled URL
        query_string = "&".join(f"{key}={value}" for key, value in payload.items())
        pre_filled_url = f"{base_url}?{query_string}"

        # Open the pre-filled form in the default web browser
        print(f"Opening form: {pre_filled_url}")
        webbrowser.open(pre_filled_url)

    def get_reason(self):
        # logger.info(self.linea_appeal_reason)
        reason = self.get_chat_gpt(self.linea_appeal_reason)
        return reason

    def get_chat_gpt(self, linea_appeal_reason):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": linea_appeal_reason}],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)

        return response.json()
