import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QListWidget, QFileDialog, 
                            QSplitter, QTabWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import openai
import fitz  # PyMuPDF

class MedicalDocument:
    """Class representing a medical document"""
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(path)
        self.text_content = self.extract_text()
        self.summary = ""
    
    def extract_text(self):
        """Extract text from PDF document"""
        try:
            doc = fitz.open(self.path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            print(f"Error extracting text from {self.path}: {e}")
            return ""

class LLMSummarizer(QThread):
    """Thread for handling LLM API calls"""
    summary_ready = pyqtSignal(str, str)  # filename, summary
    
    def __init__(self, document, api_key):
        super().__init__()
        self.document = document
        openai.api_key = api_key
        
    def run(self):
        try:
            # Simple prompt for summarization
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical assistant summarizing patient encounters. Identify key information including: date, provider, reason for visit, assessment, plan, and medications."},
                    {"role": "user", "content": f"Summarize this medical document:\n\n{self.document.text_content[:4000]}"}  # Limit for API
                ]
            )
            summary = response.choices[0].message.content
            self.document.summary = summary
            self.summary_ready.emit(self.document.filename, summary)
        except Exception as e:
            self.summary_ready.emit(self.document.filename, f"Error generating summary: {e}")

class POWParserApp(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.documents = {}  # filename -> MedicalDocument
        self.api_key = ""
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("P.O.W. Parser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left panel for document list and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Document controls
        self.upload_btn = QPushButton("Upload Documents")
        self.upload_btn.clicked.connect(self.upload_documents)
        
        self.api_key_edit = QTextEdit()
        self.api_key_edit.setPlaceholderText("Enter OpenAI API Key")
        self.api_key_edit.setMaximumHeight(60)
        
        # Document list
        self.doc_list = QListWidget()
        self.doc_list.itemClicked.connect(self.display_document)
        
        left_layout.addWidget(QLabel("OpenAI API Key:"))
        left_layout.addWidget(self.api_key_edit)
        left_layout.addWidget(self.upload_btn)
        left_layout.addWidget(QLabel("Documents:"))
        left_layout.addWidget(self.doc_list)
        left_panel.setLayout(left_layout)
        
        # Center and right area with tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Document Viewer
        doc_viewer_widget = QWidget()
        doc_viewer_layout = QVBoxLayout()
        
        splitter = QSplitter(Qt.Vertical)
        
        # Document preview area
        self.doc_preview = QTextEdit()
        self.doc_preview.setReadOnly(True)
        
        # Summary area
        summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        summary_layout.addWidget(QLabel("Document Summary:"))
        self.summary_text = QTextEdit()
        self.generate_btn = QPushButton("Generate Summary")
        self.generate_btn.clicked.connect(self.generate_summary)
        summary_layout.addWidget(self.summary_text)
        summary_layout.addWidget(self.generate_btn)
        summary_widget.setLayout(summary_layout)
        
        splitter.addWidget(self.doc_preview)
        splitter.addWidget(summary_widget)
        
        doc_viewer_layout.addWidget(splitter)
        doc_viewer_widget.setLayout(doc_viewer_layout)
        
        # Tab 2: Encounter Builder
        encounter_widget = QWidget()
        encounter_layout = QVBoxLayout()
        
        self.encounter_text = QTextEdit()
        self.encounter_text.setPlaceholderText("Build your encounter summary here...")
        
        # Buttons for encounter builder
        btn_layout = QHBoxLayout()
        self.save_encounter_btn = QPushButton("Save Encounter")
        self.save_encounter_btn.clicked.connect(self.save_encounter)
        self.clear_encounter_btn = QPushButton("Clear")
        self.clear_encounter_btn.clicked.connect(self.clear_encounter)
        btn_layout.addWidget(self.save_encounter_btn)
        btn_layout.addWidget(self.clear_encounter_btn)
        
        encounter_layout.addWidget(QLabel("Encounter Builder:"))
        encounter_layout.addWidget(self.encounter_text)
        encounter_layout.addLayout(btn_layout)
        encounter_widget.setLayout(encounter_layout)
        
        # Add tabs
        self.tabs.addTab(doc_viewer_widget, "Document Viewer")
        self.tabs.addTab(encounter_widget, "Encounter Builder")
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.tabs, 3)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def upload_documents(self):
        """Open file dialog to select and upload documents"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Medical Documents", "", "PDF Files (*.pdf)"
        )
        
        for file_path in files:
            doc = MedicalDocument(file_path)
            self.documents[doc.filename] = doc
            self.doc_list.addItem(doc.filename)
    
    def display_document(self, item):
        """Display the selected document in the preview area"""
        filename = item.text()
        if filename in self.documents:
            doc = self.documents[filename]
            self.doc_preview.setText(doc.text_content[:10000] + "...")  # Limit display for performance
            
            # Display existing summary if available
            if doc.summary:
                self.summary_text.setText(doc.summary)
            else:
                self.summary_text.clear()
    
    def generate_summary(self):
        """Generate summary for the selected document using LLM"""
        current_item = self.doc_list.currentItem()
        if not current_item:
            return
            
        filename = current_item.text()
        if filename not in self.documents:
            return
            
        # Get API key
        self.api_key = self.api_key_edit.toPlainText().strip()
        if not self.api_key:
            self.summary_text.setText("Please enter an OpenAI API key.")
            return
            
        # Update UI
        self.generate_btn.setEnabled(False)
        self.summary_text.setText("Generating summary...")
        
        # Start thread
        self.summarizer = LLMSummarizer(self.documents[filename], self.api_key)
        self.summarizer.summary_ready.connect(self.update_summary)
        self.summarizer.start()
    
    def update_summary(self, filename, summary):
        """Update the summary text when the LLM returns a result"""
        if filename in self.documents:
            self.documents[filename].summary = summary
            
        # Update UI if this is the currently displayed document
        current_item = self.doc_list.currentItem()
        if current_item and current_item.text() == filename:
            self.summary_text.setText(summary)
            
        self.generate_btn.setEnabled(True)
    
    def save_encounter(self):
        """Save the current encounter text to a file"""
        encounter_text = self.encounter_text.toPlainText()
        if not encounter_text:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Encounter", "", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(encounter_text)
            except Exception as e:
                print(f"Error saving encounter: {e}")
    
    def clear_encounter(self):
        """Clear the encounter builder text area"""
        self.encounter_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POWParserApp()
    window.show()
    sys.exit(app.exec_())