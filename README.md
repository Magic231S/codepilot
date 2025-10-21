# CodePilot — AI Tools for Developers

## 🛠️ First Tool: LegacyLens
Paste or upload legacy code → get AI explanation in Arabic & English.

## ▶️ Run Locally
1. Create `.env`:  
   `OPENAI_API_KEY=sk-...`
2. Install: `pip install -r requirements.txt`
3. Run: `uvicorn main:app --reload`
4. Open: http://localhost:8000

## ☁️ Deploy to Render
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add env var: `OPENAI_API_KEY`
