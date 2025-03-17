import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTextEdit, QListWidget, QFileDialog)
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF

class SimplePOWParser(QMainWindow):
    """A simplified version of the P.O.W. Parser application"""
    def __init__(self):
        super().__init__()
        self.documents = {}  # filename -> document text
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("Simple P.O.W. Parser")
        self.setGeometry(100, 100, 1000, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left panel - Document List
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Upload button
        self.upload_btn = QPushButton("Upload Documents")
        self.upload_btn.clicked.connect(self.upload_documents)
        
        # Document list
        self.doc_list = QListWidget()
        self.doc_list.itemClicked.connect(self.display_document)
        
        left_layout.addWidget(QLabel("Documents:"))
        left_layout.addWidget(self.upload_btn)
        left_layout.addWidget(self.doc_list)
        left_panel.setLayout(left_layout)
        
        # Right panel - Document View and Notes
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Document view
        self.doc_view = QTextEdit()
        self.doc_view.setReadOnly(True)
        
        # Encounter builder
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Add notes or build your encounter summary here...")
        
        # Save button
        self.save_btn = QPushButton("Save Notes")
        self.save_btn.clicked.connect(self.save_notes)
        
        right_layout.addWidget(QLabel("Document Content:"))
        right_layout.addWidget(self.doc_view, 3)  # Larger proportion
        right_layout.addWidget(QLabel("Encounter Notes:"))
        right_layout.addWidget(self.notes_edit, 2)  # Smaller proportion
        right_layout.addWidget(self.save_btn)
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)  # 1/4 of the width
        main_layout.addWidget(right_panel, 3)  # 3/4 of the width
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def upload_documents(self):
        """Upload and process PDF documents"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Medical Documents", "", "PDF Files (*.pdf)"
        )
        
        for file_path in files:
            filename = os.path.basename(file_path)
            
            try:
                # Extract text from the PDF
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                
                # Store document text
                self.documents[filename] = text
                
                # Add to list
                self.doc_list.addItem(filename)
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    def display_document(self, item):
        """Display the selected document in the view area"""
        filename = item.text()
        if filename in self.documents:
            # Display first 20,000 characters to avoid performance issues
            text = self.documents[filename]
            display_text = text[:20000]
            if len(text) > 20000:
                display_text += "\n\n[Document truncated due to length...]"
            
            self.doc_view.setText(display_text)
    
    def save_notes(self):
        """Save the notes/encounter text to a file"""
        notes = self.notes_edit.toPlainText()
        if not notes:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Notes", "", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(notes)
                print(f"Notes saved to {file_path}")
            except Exception as e:
                print(f"Error saving notes: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimplePOWParser()
    window.show()
    sys.exit(app.exec_())