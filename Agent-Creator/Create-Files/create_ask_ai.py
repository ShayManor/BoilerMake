from enum import Enum


class AI(Enum):
    CHATGPT = 'GPT.py'
    CLAUDE = 'Claude.py'
    DEEPSEEK = 'DeepSeek.py'


def create_ai(AI):
    with open(f'Ask_AI-Options/{AI.value}', 'r') as f:
        return f.read()
