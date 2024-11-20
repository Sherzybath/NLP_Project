import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit

from paraphraser import Paraphraser  # Import the Paraphraser class

class ParaphraserApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and geometry
        self.setWindowTitle('Paraphraser')
        self.setGeometry(100, 100, 600, 400)

        # Create layout
        self.layout = QVBoxLayout()

        # Input field for text
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText('Enter text to paraphrase')
        self.layout.addWidget(self.input_text)

        # Button to trigger paraphrasing
        self.button = QPushButton('Paraphrase', self)
        self.button.clicked.connect(self.on_paraphrase)
        self.layout.addWidget(self.button)

        # Label to display the paraphrased text
        self.output_label = QLabel('Paraphrased text will appear here.', self)
        self.layout.addWidget(self.output_label)

        # Exit Button to close the application
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)  # Close the application
        self.layout.addWidget(self.exit_button)

        # Set layout for the window
        self.setLayout(self.layout)

        # Instantiate the Paraphraser
        self.paraphraser = Paraphraser()

    def on_paraphrase(self):
        # Get the input text
        input_text = self.input_text.toPlainText()  # Use toPlainText() instead of text()

        if input_text.strip() == "":  # Check if input is empty
            self.output_label.setText("Please enter text to paraphrase.")
            return

        # Paraphrase the text using the paraphraser's method
        paraphrased_text = self.paraphraser.paraphrase_text(input_text)

        # Update the label with the paraphrased text
        self.output_label.setText(paraphrased_text)

def main():
    # Create the application and window
    app = QApplication(sys.argv)
    window = ParaphraserApp()
    window.show()
    sys.exit(app.exec_())  # Start the event loop

if __name__ == '__main__':
    main()
