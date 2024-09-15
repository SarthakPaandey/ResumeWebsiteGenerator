# It is working properly but it is not correctly hosted if you want to check it just clone and run it in your local.
# Resume Generator

## Approach and Solution

This project implements a Resume Generator web application using FastAPI. The application allows users to upload a LinkedIn PDF, select an AI API (OpenAI or Gemini), and generate an HTML resume based on the content of the PDF.

### Key Components

1. FastAPI Web Application:
   - The main application logic is implemented in `app.py`.
   - It handles file uploads, API selection, and resume generation.

2. HTML Template:
   - The upload form is defined in `templates/index.html`.
   - It provides a user-friendly interface for file upload and API selection.

3. Resume Template:
   - The generated resume uses a pre-defined HTML template (`templates/resume_template.html`).
   - This template ensures a consistent and professional look for all generated resumes.

### Running the Project Locally

To run this project on your local machine, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/SarthakPaandey/ResumeWebsiteGenerator
   cd ResumeWebsiteGenerator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv myenv
   source myenv/bin/activate  # On Windows, use: myenv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```
   uvicorn app:app --reload
   ```

5. Open your web browser and navigate to `http://127.0.0.1:8000` to access the application.

### Usage

1. Upload a LinkedIn PDF file.
2. Select the AI API you want to use (OpenAI or Gemini).
3. Enter your API key for the selected service.
4. Click "Generate Resume" to create your HTML resume.

### Dependencies

The project relies on several Python libraries, which are listed in the `requirements.txt` file.

### Future Improvements

1. Add more AI API options for resume generation.
2. Implement user authentication and resume storage.
3. Enhance the resume template with more customization options.
4. Add support for multiple file formats beyond PDF.
5. Implement a preview feature before downloading the generated resume.

This implementation provides a solid foundation for a Resume Generator application, with room for expansion and improvement based on user feedback and additional requirements.
