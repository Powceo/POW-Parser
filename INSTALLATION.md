# P.O.W. Parser Installation Guide

This guide will walk you through step-by-step instructions for setting up the P.O.W. Parser application on your computer.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Git** (optional, for cloning the repository)
   - Download from: https://git-scm.com/downloads

## Installation Steps

### Method 1: Using the Automated Setup

1. **Clone or download the repository**
   ```
   git clone https://github.com/Powceo/POW-Parser.git
   cd POW-Parser
   ```
   
   Alternatively, you can download and extract the ZIP file from the GitHub repository page.

2. **Run the setup script**
   ```
   python setup.py
   ```
   
   This script will:
   - Check your Python version
   - Create a virtual environment
   - Install all required dependencies
   - Provide instructions for activating the virtual environment

3. **Activate the virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Run the application**
   ```
   python main.py
   ```
   
   Or for the simplified version:
   ```
   python simple_pow.py
   ```

### Method 2: Manual Setup

1. **Clone or download the repository**
   ```
   git clone https://github.com/Powceo/POW-Parser.git
   cd POW-Parser
   ```

2. **Create a virtual environment (recommended)**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies manually**
   ```
   pip install PyQt5==5.15.9 PyMuPDF==1.22.5 openai==0.28.1
   ```
   
   Or using the requirements file:
   ```
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```
   python main.py
   ```

## Testing Your Installation

Before running the full application, you can test if the basic functionality works:

```
python quick_test.py path/to/your/medical_document.pdf your_openai_api_key
```

This will test:
1. PDF text extraction using PyMuPDF
2. OpenAI API connection and summarization

## Troubleshooting

### Common Issues:

1. **Error: "No module named 'PyQt5'"**
   - Make sure you've activated your virtual environment
   - Try reinstalling PyQt5: `pip install PyQt5==5.15.9`

2. **Error: "No module named 'fitz'"**
   - Install PyMuPDF: `pip install PyMuPDF==1.22.5`

3. **PDF Extraction Errors**
   - Make sure the PDF is not password-protected
   - Try with a different PDF file

4. **OpenAI API Errors**
   - Verify your API key is correct
   - Check your internet connection
   - Make sure your OpenAI account has API access and credits

### Need Help?

If you encounter any issues not covered here, please:
1. Check the GitHub repository issues section for similar problems
2. Create a new issue describing your problem with detailed information

## Using the Application

1. Enter your OpenAI API key in the text field (for main.py version)
2. Click "Upload Documents" to select PDF files
3. Select a document from the list to view its contents
4. Click "Generate Summary" to create an AI summary (for main.py version)
5. Use the "Encounter Builder" tab to compile information from multiple documents
6. Save your work using the "Save" button