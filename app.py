from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add the CORS middleware immediately after initializing the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the templates directory
templates = Jinja2Templates(directory="templates")

# Mount the static files directory (if you have any static files)
app.mount("/static", StaticFiles(directory="static"), name="static")

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class APIRequest(BaseModel):
    api_key: str
    api_selection: str

@app.post("/")
async def upload_file(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    api_selection: str = Form(...)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file part")
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")
    if file and allowed_file(file.filename):
        try:
            # Read the PDF file
            pdf_reader = PdfReader(io.BytesIO(await file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Use the form data directly
            if not api_key:
                raise HTTPException(status_code=400, detail="No API key provided")

            if api_selection == 'openai':
                # Use OpenAI API
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates HTML resumes."},
                        {"role": "user", "content": f"Generate an HTML resume based on the following text extracted from a LinkedIn PDF: {text}"}
                    ]
                )
                resume_data = response.choices[0].message.content
            elif api_selection == 'gemini':
                # Use Gemini API
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Generate an HTML resume based on the following text extracted from a LinkedIn PDF: {text}"
                response = model.generate_content(prompt)
                resume_data = response.text
            else:
                raise HTTPException(status_code=400, detail="Invalid API selection")

            # Save HTML content to a file
            filename = file.filename.rsplit('.', 1)[0] + '.html'
            with open(filename, 'w') as f:
                f.write(resume_data)

            return FileResponse(filename, filename=filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Allowed file type is PDF")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error_message": exc.detail},
        status_code=exc.status_code
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)