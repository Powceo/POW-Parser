"""
A simple script to test the basic functionality of extracting text from PDFs 
and generating summaries using OpenAI GPT.

This is useful for testing that your environment is set up correctly
before running the full application.
"""
import os
import sys
import fitz  # PyMuPDF
import openai

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        print(f"Opening PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        
        text = ""
        for i, page in enumerate(doc):
            print(f"Processing page {i+1}/{len(doc)}")
            text += page.get_text()
        
        print(f"Successfully extracted {len(text)} characters from PDF")
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def generate_summary(text, api_key):
    """Generate a summary using OpenAI API"""
    try:
        print("Connecting to OpenAI API...")
        openai.api_key = api_key
        
        # Use just a portion of the text to stay within token limits
        sample = text[:4000]
        
        print("Sending request to OpenAI...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical assistant summarizing patient encounters. Identify key information including: date, provider, reason for visit, assessment, plan, and medications."},
                {"role": "user", "content": f"Summarize this medical document:\n\n{sample}"}
            ]
        )
        
        summary = response.choices[0].message.content
        print("\nSummary generated successfully!")
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

def main():
    # Check if a PDF file path was provided
    if len(sys.argv) < 2:
        print("Usage: python quick_test.py <path_to_pdf_file> [openai_api_key]")
        return
    
    pdf_path = sys.argv[1]
    
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    # Extract text from PDF
    print("\n=== PDF TEXT EXTRACTION TEST ===\n")
    text = extract_text_from_pdf(pdf_path)
    
    if text:
        print("\n--- First 500 characters of extracted text ---")
        print(text[:500])
        print("...")
        print("--- End of preview ---\n")
    else:
        print("Failed to extract text from PDF.")
        return
    
    # Check if an API key was provided
    if len(sys.argv) >= 3:
        api_key = sys.argv[2]
        
        # Generate summary
        print("\n=== OPENAI SUMMARY GENERATION TEST ===\n")
        summary = generate_summary(text, api_key)
        
        if summary:
            print("\n--- Generated Summary ---")
            print(summary)
            print("--- End of summary ---\n")
        else:
            print("Failed to generate summary.")
    else:
        print("\nNo OpenAI API key provided. Skipping summary generation test.")
        print("To test summary generation, run:")
        print(f"python quick_test.py \"{pdf_path}\" your_openai_api_key")

if __name__ == "__main__":
    main()