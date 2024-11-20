import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from summarizer import summarize_text
from paraphraser import Paraphraser
from translator import translate_english_to_hindi,translate_hindi_to_english

class HomePage(QWidget):
    def __init__(self, navigate_to_paraphraser, navigate_to_summarizer,navigate_to_translator, navigate_to_translator2, custom_font):
        super().__init__()

        # Layout for the homepage
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Welcome message (make it very big)
        welcome_label = QLabel("Welcome to Raviel")
        welcome_label.setFont(QFont(custom_font.family(), 38, QFont.Bold))  # Larger font size
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Paraphraser button
        paraphrase_button = QPushButton("Paraphraser")
        paraphrase_button.setFont(custom_font)
        paraphrase_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: white;
                color: #3c3c3c;
            }
        """)
        paraphrase_button.clicked.connect(navigate_to_paraphraser)
        layout.addWidget(paraphrase_button)

        # Summarizer button
        summarizer_button = QPushButton("Summarizer")
        summarizer_button.setFont(custom_font)
        summarizer_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: white;
                color: #3c3c3c;
            }
        """)
        summarizer_button.clicked.connect(navigate_to_summarizer)
        layout.addWidget(summarizer_button)

        self.setLayout(layout)
        # Translator
        translator_button = QPushButton("English to Hindi")
        translator_button.setFont(custom_font)
        translator_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: white;
                color: #3c3c3c;
            }
        """)
        translator_button.clicked.connect(navigate_to_translator)
        layout.addWidget(translator_button)

        self.setLayout(layout)
        # BACKUP
        # BACKUP
        # BACKUP
        # BACKUP
        translator2_button = QPushButton("Hindi to English")
        translator2_button.setFont(custom_font)
        translator2_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: white;
                color: #3c3c3c;
            }
        """)
        translator2_button.clicked.connect(navigate_to_translator2)
        layout.addWidget(translator2_button)

        self.setLayout(layout)


class TextProcessorPage(QWidget):
    def __init__(self, title, process_function, custom_font, navigate_back):
        super().__init__()

        # Layout for the processor page
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Page title
        title_label = QLabel(title)
        title_label.setFont(custom_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Input text field
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter your text here...")
        self.input_text.setFont(custom_font)
        layout.addWidget(self.input_text)

        # Process button
        process_button = QPushButton(f"Run {title}")
        process_button.setFont(custom_font)
        process_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: #3c3c3c;
            }
        """)
        process_button.clicked.connect(self.process_text)
        layout.addWidget(process_button)

        # Output text field
        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText("Output will appear here...")
        self.output_text.setReadOnly(True)
        self.output_text.setFont(custom_font)
        layout.addWidget(self.output_text)

        # Back button
        back_button = QPushButton("Back")
        back_button.setFont(custom_font)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: #3c3c3c;
            }
        """)
        back_button.clicked.connect(navigate_back)
        layout.addWidget(back_button)

        # Save the process function
        self.process_function = process_function

        self.setLayout(layout)

    def process_text(self):
        input_text = self.input_text.toPlainText()
        if not input_text.strip():
            self.output_text.setText("Please enter text to process.")
            return

        # Process the input text
        result = self.process_function(input_text)
        self.output_text.setText(result)


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont(r"C:\Users\sdzyr\Desktop\Project\NLP\Lancea.otf")
        if font_id == -1:
            print("Failed to load the custom font.")
            custom_font = QFont("Arial", 12)  # Fallback to default font
        else:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(family, 14)

        # Set up the main window
        self.setWindowTitle("Raviel")
        self.setGeometry(100, 100, 800, 600)

        # Stacked widget for navigation
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # Create the pages
        self.home_page = HomePage(self.show_paraphraser_page, self.show_summarizer_page, self.show_translator_page, self.show_translator2_page, custom_font)
        self.paraphraser_page = TextProcessorPage(
            "Paraphraser", self.paraphrase_text, custom_font, self.show_home_page
        )
        self.summarizer_page = TextProcessorPage(
            "Summarizer", self.summarize_text, custom_font, self.show_home_page
        )
        self.translator_page = TextProcessorPage(
            "Translator", self.translator, custom_font, self.show_home_page
        )
        self.translator2_page = TextProcessorPage(
            "Translator", self.translator2, custom_font, self.show_home_page
        )

        # Add pages to the stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.paraphraser_page)
        self.stack.addWidget(self.summarizer_page)
        self.stack.addWidget(self.translator_page)
        self.stack.addWidget(self.translator2_page)
        # Set initial page
        self.stack.setCurrentWidget(self.home_page)

        # Paraphraser instance
        self.paraphraser = Paraphraser()

    def show_home_page(self):
        self.stack.setCurrentWidget(self.home_page)

    def show_paraphraser_page(self):
        self.stack.setCurrentWidget(self.paraphraser_page)

    def show_summarizer_page(self):
        self.stack.setCurrentWidget(self.summarizer_page)
    def show_translator_page(self):
        self.stack.setCurrentWidget(self.translator_page)
    def show_translator2_page(self):
        self.stack.setCurrentWidget(self.translator2_page)
    
    def paraphrase_text(self, text):
        return self.paraphraser.paraphrase_text(text)
 
    def summarize_text(self, text):
        return summarize_text(text)
    def translator(self, text):
        return translate_english_to_hindi(text)
    def translator2(self, text):
        return translate_hindi_to_english(text)
def main():
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
