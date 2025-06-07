class ChatHistory:
    def __init__(self):
        self.history = []

    def add_user_message(self, msg):
        self.history.append({"role": "user", "content": msg})

    def add_bot_message(self, msg):
        self.history.append({"role": "assistant", "content": msg})

    def get_prompt(self):
        formatted = ""
        for h in self.history:
            prefix = "Usuário:" if h["role"] == "user" else "Assistente:"
            formatted += f"{prefix} {h['content']}\n"
        return formatted