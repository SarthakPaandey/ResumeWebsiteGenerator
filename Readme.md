# Resume Generator

## Approach and Solution

This project implements a Resume Generator web application using Flask. The application allows users to upload a LinkedIn PDF, select an AI API (OpenAI or Gemini), and generate an HTML resume based on the content of the PDF.

### Key Components

1. Flask Web Application:
   - The main application logic is implemented in `app.py`.
   - It handles file uploads, API selection, and resume generation.

2. HTML Template:
   - The upload form is defined in `templates/upload.html`.
   - It provides a user-friendly interface for file upload and API selection.

3. Resume Template:
   - The generated resume uses a pre-defined HTML template (`templates/resume_template.html`).
   - This template ensures a consistent and professional look for all generated resumes.

### Implementation Details

1. File Upload and Validation:
   - The application accepts PDF files only.
   - File validation is performed using the `allowed_file` function.

2. PDF Text Extraction:
   - PyPDF2 library is used to extract text from the uploaded PDF.

3. AI API Integration:
   - The application supports two AI APIs: OpenAI and Gemini.
   - API selection is done through radio buttons in the upload form.
   - The selected API is used to generate the resume content based on the extracted PDF text.

4. Resume Generation:
   - The AI-generated content is inserted into the HTML template.
   - The resulting HTML file is saved and sent back to the user for download.

5. Error Handling:
   - The application includes error handling for various scenarios, such as missing files, invalid file types, and API errors.
   - Flash messages are used to communicate errors to the user.

6. Security Considerations:
   - The `secure_filename` function is used to ensure safe filenames.
   - API keys are obtained from the user input rather than being hardcoded.

### Code Structure

The main application logic is contained in the `upload_file` function:

### User Interface

The user interface is designed to be simple and intuitive:


### Dependencies

The project relies on several Python libraries, which are listed in the `requirements.txt` file:


### Future Improvements

1. Add more AI API options for resume generation.
2. Implement user authentication and resume storage.
3. Enhance the resume template with more customization options.
4. Add support for multiple file formats beyond PDF.
5. Implement a preview feature before downloading the generated resume.

This implementation provides a solid foundation for a Resume Generator application, with room for expansion and improvement based on user feedback and additional requirements.
