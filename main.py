from llama_cpp import Llama
from flask import Flask, request, jsonify, render_template
import os
import sys

MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
if not os.path.exists(MODEL_PATH): raise ValueError(f"Caminho do modelo não existe: {MODEL_PATH}")

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def get_excel_assistant_response(user_input: str) -> str:
    """Processa a pergunta sobre Excel e retorna a resposta do modelo"""
    if user_input.lower() in ["sair", "exit", "quit"]: return "Até logo! Fico à disposição para ajudar com Excel quando precisar."
    prompt = f"""Responda como um especialista em Excel\nResposta:"
{user_input}

Resposta:"""

    output = llm(prompt, max_tokens=512, stop=["Usuário:", "Você:"])
    return output["choices"][0]["text"].strip()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

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