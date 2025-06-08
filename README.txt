== Excel Chatbot Local (com Mistral 7B Instruct GGUF) ==
0. Linux pre-req:
`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

0.1. Clonando via terminal:
   `git clone https://github.com/felipesaugusto/chatbot`

1. Instale as dependências (Python 3.10 ou superior recomendado):
   pip install -r requirements.txt
   llama-cpp
   flask

2. Baixe um modelo do Mistral 7B aqui:
   https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

   Utilizamos o modelo `mistral-7b-instruct-v0.1.Q4_K_M.gguf` nas nossas execuções pois ele possui qualidade/tamanhos balanceados
   Caso baixe outro modelo, basta alterar o "path" do modelo no arquivo `main.py` (linha 6) 
   E coloque dentro da pasta: **models/**

3. Para executar o chatbot...
   via terminal:
      python main.py
   via Web/navegador:
      python main.py --web
   
Durante a execução, digite sua dúvida sobre Excel. Para sair, digite: sair



