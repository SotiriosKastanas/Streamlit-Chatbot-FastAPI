# Streamlit Chatbot + FastAPI

Streamlit frontend connected to a FastAPI backend that handles LLM calls.

## Install
```bash
pip install -r requirements.txt
```
## Environmental Variables
Create a .env file in the project root (required for LLM credentials - Azure OpenAI):
```bash
OPENAI_API_KEY=...
OPENAI_ENDPOINT=...
OPENAI_API_VERSION=...
OPENAI_DEPLOYMENT_NAME=...
```
## Run
Terminal 1 (Backend)
```bash
uvicorn backend.main:app --reload
```
Terminal 2 (Frontend)
```bash
streamlit run .\frontend\app.py
```

