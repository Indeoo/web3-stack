import requests


class AIChat:
    def ask(self, question):
        pass


class ChatGPT:
    def __init__(self, token):
        self.token = token

    def ask(self, question):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)

        return response.json()
