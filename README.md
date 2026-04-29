# AutoBot — Automobile Help Desk Chatbot
 
An AI-powered chatbot that helps everyday car owners troubleshoot common vehicle
problems in plain English.
 
## Setup Instructions
 
### Step 1 — Get a Free Grok API Key
1. Go to https://console.x.ai
2. Sign up for a free account
3. Create an API key under "API Keys"
 
### Step 2 — Install Python Dependencies
```
pip install -r requirements.txt
```
 
### Step 3 — Add Your API Key
Open the .env file and replace the placeholder:
```
XAI_API_KEY=your-actual-api-key-here
```
 
### Step 4 — Run the Chatbot
```
streamlit run app.py
```
Opens in your browser at http://localhost:8501
 
### Step 5 — Run Tests
```
python -m unittest tests.py -v
```
 
## Project Structure
- app.py — Streamlit web interface
- chat_engine.py — LLM logic, RAG search, validation
- knowledge_base.txt — 11 car problem sections for RAG
- system_prompt.txt — AutoBot persona and rules
- tests.py — 10 unit tests
- requirements.txt — Python dependencies
- .env — API key (never commit this)
 
## Technology Stack
- Python 3.13, Streamlit, xAI Grok API (free tier), python-dotenv
