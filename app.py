from flask import Flask, render_template_string, request, send_file
import os
from striprtf.striprtf import rtf_to_text
from datetime import datetime
from PIL import Image
from fpdf import FPDF
from PyPDF2 import PdfMerger
import tempfile
import threading

app = Flask(__name__)

# Create folders for uploads and converted files
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Allowed extensions for files for the first app
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'pdf'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to convert images to PDF
def convert_images_to_pdf(images):
    pdf = FPDF()

    for image_path in images:
        img = Image.open(image_path)
        width, height = img.size
        aspect_ratio = width / height
        pdf_width = 210  # A4 width in mm
        pdf_height = 297  # A4 height in mm
        pdf_height = pdf_width / aspect_ratio if aspect_ratio > 1 else pdf_height
        pdf.add_page()
        pdf.image(image_path, 0, 0, pdf_width, pdf_height)

    return pdf

# Function to merge PDF files
def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    return merger

# Function for cleanup after sending the file
def cleanup_files(files):
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

# Home route
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route for the first app (upload images and PDFs)
@app.route('/upload_images_pdfs', methods=['POST'])
def upload_images_pdfs():
    if 'file' not in request.files:
        return 'No file part', 400

    files = request.files.getlist('file')

    if len(files) == 0:
        return 'No selected files', 400

    image_files = []
    pdf_files = []

    for file in files:
        if file and allowed_file(file.filename):
            if file.filename.lower().endswith(('.jpg', '.jpeg')):
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                file.save(temp_file.name)
                image_files.append(temp_file.name)
            elif file.filename.lower().endswith('.pdf'):
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                file.save(temp_file.name)
                pdf_files.append(temp_file.name)

    image_pdf = convert_images_to_pdf(image_files)

    image_pdf_path = tempfile.mktemp(suffix='.pdf')
    image_pdf.output(image_pdf_path)

    image_pdf.close()

    all_pdf_files = pdf_files + [image_pdf_path]

    merged_pdf = merge_pdfs(all_pdf_files)

    final_pdf_path = tempfile.mktemp(suffix='.pdf')
    merged_pdf.write(final_pdf_path)

    cleanup_thread = threading.Thread(target=cleanup_files, args=(image_files + pdf_files + [image_pdf_path],))
    cleanup_thread.start()

    return send_file(final_pdf_path, as_attachment=True, download_name='combined_output.pdf')

# Route for the second app (upload RTF files)
@app.route('/upload_rtf', methods=['POST'])
def upload_rtf():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    converted_filepath = convert_rtf_to_utf8(filepath, file.filename)

    return send_file(converted_filepath, as_attachment=True)

# Function to convert RTF to UTF-8
def convert_rtf_to_utf8(input_filepath, original_filename):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    base_filename = os.path.splitext(original_filename)[0]
    output_filename = f"{base_filename}_{current_time}_converted.txt"
    output_filepath = os.path.join(CONVERTED_FOLDER, output_filename)

    with open(input_filepath, 'r', encoding='latin1') as infile:
        rtf_content = infile.read()

    plain_text = rtf_to_text(rtf_content)

    header = f"Converted from: {original_filename}\nDate-time: {current_time}\n\n"
    plain_text_with_header = header + plain_text

    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(plain_text_with_header)

    return output_filepath

# HTML Template for UI with two tabs
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Converter</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Lora:wght@400;700&family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }

        .container {
            width: 80%;
            margin: 0 auto;
            padding: 20px;
        }

        /* Tab container */
        .tabs {
            display: flex;
            background-color: #f4f4f9;
            border-radius: 10px 10px 0 0;
            overflow: hidden;
        }

        /* Common tab styles */
        .tab {
            padding: 14px 20px;
            flex: 1;
            text-align: center;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.3s;
        }

        .tab:hover {
            opacity: 0.8;
        }

        /* Specific styles for each tab */
        .tab-blue {
            background-color: #007BFF;
            color: white;
        }

        .tab-green {
            background-color: #28a745;
            color: white;
        }

        .tab-blue.active {
            background-color: #0056b3;
        }

        .tab-green.active {
            background-color: #218838;
        }

        /* Tab content container */
        .tab-content {
            display: none;
            padding: 30px 20px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: #333;
        }

        .tab-blue-content {
            background-color: #e6f4ff; /* Light blue background for the blue tab */
        }

        .tab-green-content {
            background-color: #e2f9e1; /* Light green background for the green tab */
        }

        .tab-content.active {
            display: block;
        }

        h2 {
            font-family: 'Montserrat', sans-serif;
            font-size: 26px;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        input[type="file"] {
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
            background-color: #f9f9f9;
        }

        button {
            padding: 12px 20px;
            background-color: #007BFF;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #777;
        }

        footer a {
            color: #007BFF;
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="tabs">
        <div class="tab tab-blue" onclick="showTab(0)">Images/PDF to Combined PDF</div>
        <div class="tab tab-green" onclick="showTab(1)">RTF to UTF-8 Text</div>
    </div>

    <div class="tab-content tab-blue-content" id="tab1">
        <h2>Convert Images/PDFs to a Combined PDF</h2>
        <form action="/upload_images_pdfs" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <input type="file" name="file" accept=".jpg,.jpeg,.pdf" multiple required>
            </div>
            <button type="submit">Upload and Convert</button>
        </form>
    </div>

    <div class="tab-content tab-green-content" id="tab2">
        <h2>Convert RTF to UTF-8 Text</h2>
        <form action="/upload_rtf" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <input type="file" name="file" accept=".rtf" required>
            </div>
            <button type="submit">Upload and Convert</button>
        </form>
    </div>
</div>

<footer>
    <p>Powered by <a href="https://www.yourcompany.com" target="_blank">Abhijeet Arde</a></p>
</footer>

<script>
    function showTab(tabIndex) {
        const tabs = document.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll('.tab-content');

        tabs.forEach((tab, index) => {
            tab.classList.remove('active');
            if (index === tabIndex) {
                tab.classList.add('active');
            }
        });

        tabContents.forEach((content, index) => {
            content.classList.remove('active');
            if (index === tabIndex) {
                content.classList.add('active');
            }
        });
    }

    // Set default active tab
    showTab(0);
</script>

</body>
</html>

'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
