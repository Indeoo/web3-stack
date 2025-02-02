import requests

from web3_wizzard_lib.core.utils.benchmark_utils import benchmark


class AIChat:
    def ask(self, question):
        pass


class ChatGPT:
    def __init__(self, token):
        self.token = token

    @benchmark
    def ask(self, question):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        data = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)

        return response.json()['choices'][0]['message']['content']


class MockAIChat:
    def __init__(self, token):
        self.token = token

    def ask(self, question):
        return f"ANSWER {question}"


def get_ai_chat(ai_config, token):
    if ai_config == 'CHAT_GPT':
        return ChatGPT(token)
    else:
        return MockAIChat(token)
