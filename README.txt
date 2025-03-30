PDF Extraction App

Overview

This is a PDF Extraction App that allows users to extract text and images from PDF files. The project is built using Python, PyMuPDF (fitz), and Kivy to provide a graphical user interface (GUI) for selecting PDFs and extracting content.

Features

Extract Text from selected PDF files.

Extract Images from selected PDF files.

Simple UI built using Kivy.

Cross-platform support (Windows, Linux, macOS, Android).

Technologies Used

Python 3

Kivy (for UI development)

PyMuPDF (fitz) (for PDF processing)

PIL (Pillow) (for handling images)

Installation

1. Clone the Repository

cd pdf-extraction-app

2. Install Dependencies

pip install -r requirements.txt

3. Run the Application

python pdf_extraction_app.py

How to Use

Open the application.

Select a PDF file using the file picker.

Click Extract Text or Extract Images to retrieve content.

The extracted text will be displayed, and images will be saved in a folder.

Convert to Mobile App (Android)

To package the app as an Android APK, use buildozer:

pip install buildozer
buildozer init
buildozer -v android debug

This will generate an APK file that can be installed on an Android device.

License

This project is licensed under the MIT License.

Contributing

Feel free to contribute by submitting issues or pull requests!

Author

Manoj D📧 Email: manojdayalan1107@gmail.com🔗 GitHub: MAN-MANOJ
