# File Converter Web Application

This web application, built using Flask, provides two separate file conversion functionalities:

1. **Images/PDF to Combined PDF**: Upload images (JPG, JPEG) and PDFs, and merge them into a single PDF.
2. **RTF to UTF-8 Text**: Upload RTF (Rich Text Format) files, and convert them into UTF-8 encoded text files.

## Features

- **Tab-based UI**: The application has a tabbed interface for two distinct conversion tasks.
  - **Tab 1**: Converts images and PDFs into a combined PDF document.
  - **Tab 2**: Converts RTF files into clean UTF-8 encoded text.
  
- **PDF Conversion**: Combines multiple images and PDFs into a single PDF document.
- **RTF Conversion**: Converts RTF files to plain text, adding conversion metadata (e.g., timestamp).
- **Responsive Design**: The UI is mobile-friendly, adapting to different screen sizes for a seamless user experience.
- **Temporary File Cleanup**: Automatically deletes temporary files after use to maintain efficiency.

## Technologies Used

- **Flask**: Web framework for building the backend.
- **Python**: The programming language used for backend development.
- **FPDF**: Used to generate PDFs from images.
- **PIL (Pillow)**: Used for handling images and converting them into PDF format.
- **PyPDF2**: Merges multiple PDF files into a single document.
- **striprtf**: Converts RTF files to plain text.
- **Bootstrap** (via custom CSS): For UI layout and design.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- Pillow
- FPDF
- PyPDF2
- striprtf

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/file-converter-app.git
    cd file-converter-app
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    Or install them manually using:

    ```bash
    pip install flask pillow fpdf pypdf2 striprtf
    ```

4. Run the Flask app:

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:9000`.

## Usage

1. **Open the application** in a web browser at `http://127.0.0.1:9000`.
   
### Tab 1: **Images/PDF to Combined PDF**

- **Purpose**: Combine multiple images (JPG, JPEG) and PDFs into a single PDF document.
- **How it works**:
  - You can upload one or more image files (JPG, JPEG) and PDF files.
  - The uploaded images will be converted into PDF pages and merged with the uploaded PDFs.
  - Once the files are combined, a single PDF will be generated and available for download.
  
### Tab 2: **RTF to UTF-8 Text**

- **Purpose**: Convert an RTF (Rich Text Format) file into a clean, UTF-8 encoded text file.
- **How it works**:
  - Upload an RTF file.
  - The RTF content will be stripped of formatting and converted to plain text with UTF-8 encoding.
  - A header, including the original filename and conversion timestamp, will be added to the text file.
  - The converted text file will be available for download.

## File Handling

- **Uploads Folder**: Uploaded files are temporarily stored in the `uploads/` folder.
- **Converted Files**: Converted files are stored in the `converted_files/` folder.
- **Temporary Files**: Temporary files are created during conversion and automatically deleted after the user downloads the final file.

## Folder Structure

