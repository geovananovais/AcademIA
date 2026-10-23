# AcademIA 💪

Personal trainer virtual com IA (Flask + OpenAI).

## Como rodar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
2. Copie `.env.example` para `.env` e preencha:
   ```
   OPENAI_API_KEY=sua-chave
   SECRET_KEY=uma-chave-aleatoria
   ```
   Para gerar a `SECRET_KEY`:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Inicie o servidor:
   ```
   python app.py
   ```
4. Acesse http://localhost:5001

> Os dados dos usuários são salvos em `data/usuarios.json` (criado automaticamente e ignorado pelo Git).
