from llama_cpp import Llama
from flask import Flask, request, jsonify, render_template_string
import os
import sys

MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

if not os.path.exists(MODEL_PATH):
    raise ValueError(f"Caminho do modelo não existe: {MODEL_PATH}")

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def get_excel_assistant_response(user_input: str) -> str:
    """Processa a pergunta sobre Excel e retorna a resposta do modelo"""
    if user_input.lower() in ["sair", "exit", "quit"]:
        return "Até logo! Fico à disposição para ajudar com Excel quando precisar."

    prompt = f"""Você é um assistente especializado em Microsoft Excel. Dê exemplos práticos quando possível e mantenha a conversa fluida, fazendo perguntas ao final para manter o usuário engajado. Ajude o usuário com a seguinte dúvida:
{user_input}

Resposta:"""

    output = llm(prompt, max_tokens=512, stop=["Usuário:", "Você:"])
    return output["choices"][0]["text"].strip()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template_string('''
        <!DOCTYPE html>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Excel Assistant</title>
    <style>
        * {
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 20px;
    display: flex;
    justify-content: center;
}

h1 {
    color: #2e7d32;
    text-align: center;
    margin-bottom: 20px;
}

#chat-container {
    width: 100%;
    max-width: 800px;
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 15px;
}

#chatbox {
    height: 400px;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #ffffff;
}

.message {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 15px;
    line-height: 1.5;
    word-wrap: break-word;
    white-space: pre-wrap;
}

.user-message {
    align-self: flex-end;
    background-color: #d1e7dd;
    color: #0c4128;
    border-bottom-right-radius: 4px;
}

.bot-message {
    align-self: flex-start;
    background-color: #f1f1f1;
    color: #111;
    border-bottom-left-radius: 4px;
}

#input-container {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

#user-input {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid #ccc;
    border-radius: 20px;
    font-size: 16px;
    outline: none;
}

#user-input:focus {
    border-color: #4CAF50;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #45a049;
}

    </style>
</head>
<body>
    <div id="chat-container">
        <h1>Excel Assistant</h1>
        <div id="chatbox"></div>
        <div id="input-container">
            <input type="text" id="user-input" placeholder="Pergunte algo sobre Excel..." autofocus>
            <button id="send-btn">Enviar</button>
        </div>
    </div>

    <script>
        const chatbox = document.getElementById('chatbox');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');

        // Mensagem inicial
        addBotMessage('Olá! Sou seu assistente especializado em Excel. Como posso te ajudar hoje?');

        function addBotMessage(message) {
            addMessage(message, 'bot');
        }

        function addUserMessage(message) {
            addMessage(message, 'user');
        }


        function addMessage(message, type) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;

            const contentDiv = document.createElement('div');
            contentDiv.textContent = message;

            messageDiv.appendChild(contentDiv);
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }


        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            addUserMessage(message);
            userInput.value = '';
            userInput.disabled = true;
            sendBtn.disabled = true;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message })
                });

                const data = await response.json();
                addBotMessage(data.response);
            } catch (e) {
                addBotMessage("Desculpe, ocorreu um erro ao tentar responder.");
            }

            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }

        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
    ''')

@app.route("/chat", methods=["POST"])
def chat_api():
    """Endpoint da API para o chat"""
    data = request.json
    user_message = data.get("message", "")
    response = get_excel_assistant_response(user_message)
    return jsonify({"response": response})

def terminal_chat():
    print("\n=== Excel Chatbot ===")
    print("Digite sua pergunta sobre Excel (ou 'sair' para encerrar)\n")
    
    while True:
        user_input = input("Você: ")
        resposta = get_excel_assistant_response(user_input)
        print("Assistente:", resposta)
        
        if user_input.lower() in ["sair", "exit", "quit"]:
            break

if __name__ == "__main__":
    if "--web" in sys.argv:
        print("Iniciando servidor web... Acesse http://localhost:5000")
        app.run(host="0.0.0.0", port=5000)
    else:
        terminal_chat()