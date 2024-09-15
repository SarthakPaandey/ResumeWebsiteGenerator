from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import os
import openai
from PyPDF2 import PdfReader
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
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

                # Get OpenAI API key
                api_key = request.form['api_key']
                if not api_key:
                    flash('No API key provided')
                    return redirect(request.url)

                openai.api_key = api_key

                # Use OpenAI to generate HTML resume
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that generates HTML resumes. Use the provided template structure."},
                            {"role": "user", "content": f"Generate an HTML resume based on the following text extracted from a LinkedIn PDF: {text}"}
                        ]
                    )

                    resume_data = response.choices[0].message['content']

                    # Render the template with the generated data
                    html_content = render_template('resume_template.html', **resume_data)

                    # Save HTML content to a file
                    filename = secure_filename(file.filename.rsplit('.', 1)[0] + '.html')
                    with open(filename, 'w') as f:
                        f.write(html_content)

                    return send_file(filename, as_attachment=True)
                except openai.error.OpenAIError as e:
                    flash(f'OpenAI API error: {str(e)}')
                    return redirect(request.url)

            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Allowed file type is PDF')
            return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)