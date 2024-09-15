from flask import Flask, request, render_template, send_file, flash, redirect
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
from werkzeug.utils import secure_filename
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                # Read the PDF file
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()

                # Get API key and selected API
                api_key = request.form['api_key']
                selected_api = request.form['api_selection']

                if not api_key:
                    flash('No API key provided')
                    return redirect(request.url)

                if selected_api == 'openai':
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
                elif selected_api == 'gemini':
                    # Use Gemini API
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-pro')
                    prompt = f"Generate an HTML resume based on the following text extracted from a LinkedIn PDF: {text}"
                    response = model.generate_content(prompt)
                    resume_data = response.text
                else:
                    flash('Invalid API selection')
                    return redirect(request.url)

                print("Generated resume data:", resume_data) 

                
                html_content = resume_data  

                # Save HTML content to a file
                filename = secure_filename(file.filename.rsplit('.', 1)[0] + '.html')
                with open(filename, 'w') as f:
                    f.write(html_content)

                return send_file(filename, as_attachment=True)
            except Exception as e:
                print(f"Detailed error: {str(e)}") 
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Allowed file type is PDF')
            return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)