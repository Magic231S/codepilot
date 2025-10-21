import os
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def analyze_code_with_ai(code: str) -> str:
    prompt = f"""
    You are a senior bilingual developer (Arabic/English).
    Explain this code clearly in both languages:

    - What does it do?
    - Any security risks?
    - How would you modernize it?

    Code:
    {code[:3500]}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/tools/legacylens", response_class=HTMLResponse)
async def legacylens_page(request: Request):
    return templates.TemplateResponse("legacylens.html", {"request": request})

@app.post("/tools/legacylens/analyze", response_class=HTMLResponse)
async def analyze_code(
    request: Request,
    code: str = Form(""),
    file: UploadFile = File(None)
):
    if not code and not file:
        return templates.TemplateResponse("legacylens.html", {
            "request": request,
            "error": "Please provide code or upload a file."
        })
    
    if file:
        content = (await file.read()).decode('utf-8')
    else:
        content = code

    explanation = analyze_code_with_ai(content)
    return templates.TemplateResponse("legacylens.html", {
        "request": request,
        "explanation": explanation
    })
