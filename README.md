# P.O.W. Parser

A simple application for parsing and summarizing medical documents, creating encounter summaries, and organizing medical information.

## Features

- Upload and view PDF medical documents
- Extract text from medical PDFs
- Generate summaries of medical encounters using OpenAI's GPT models
- Build and save comprehensive encounter reports

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Powceo/POW-Parser.git
   cd POW-Parser
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```
   
   Or for a simplified version:
   ```
   python simple_pow.py
   ```

2. Enter your OpenAI API key in the designated field
3. Upload medical documents using the "Upload Documents" button
4. Click on a document in the list to view its contents
5. Click "Generate Summary" to create an AI-generated summary of the document
6. Use the "Encounter Builder" tab to compile information from multiple documents
7. Save your compiled encounter using the "Save Encounter" button

## Requirements

- Python 3.8 or higher
- PyQt5
- PyMuPDF (for PDF processing)
- OpenAI API key

## Testing

To test basic functionality before running the full application:

```
python quick_test.py path/to/your/medical_document.pdf your_openai_api_key
```

This will verify that PDF extraction and OpenAI API integration are working correctly.
