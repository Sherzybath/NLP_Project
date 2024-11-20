import sys
import math
import re
import urllib.request
import bs4 as bs
from PyPDF2 import PdfReader
import nltk
from nltk.stem import WordNetLemmatizer
import spacy
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QComboBox, QFileDialog, QMessageBox

# Download wordnet if not already available
nltk.download('wordnet')

# Initialize spaCy and lemmatizer
nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()


# Function to read text from .txt file
def file_text(filepath):
    with open(filepath, 'r') as f:
        return f.read().replace("\n", '')


# Function to read text from PDF file
def pdfReader(pdf_path):
    with open(pdf_path, 'rb') as pdfFileObject:
        pdfReader = PdfReader(pdfFileObject)
        text = ""
        for page in pdfReader.pages:
            text += page.extract_text() or ""
    return text


# Function to read text from Wikipedia URL
def wiki_text(url):
    scrap_data = urllib.request.urlopen(url)
    article = scrap_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    article_text = re.sub(r'\[[0-9]*\]', '', article_text)
    return article_text


# Text summarization functions (Your original functions)
def frequency_matrix(sentences):
    freq_matrix = {}
    stopWords = nlp.Defaults.stop_words
    for sent in sentences:
        freq_table = {}
        words = [word.text.lower() for word in sent if word.text.isalnum()]
        for word in words:
            word = lemmatizer.lemmatize(word)
            if word not in stopWords:
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1
        freq_matrix[sent[:15]] = freq_table
    return freq_matrix


def tf_matrix(freq_matrix):
    tf_matrix = {}
    for sent, freq_table in freq_matrix.items():
        tf_table = {}
        total_words = len(freq_table)
        for word, count in freq_table.items():
            tf_table[word] = count / total_words
        tf_matrix[sent] = tf_table
    return tf_matrix


def sentences_per_words(freq_matrix):
    sent_per_words = {}
    for sent, f_table in freq_matrix.items():
        for word in f_table.keys():
            sent_per_words[word] = sent_per_words.get(word, 0) + 1
    return sent_per_words


def idf_matrix(freq_matrix, sent_per_words, total_sentences):
    idf_matrix = {}
    for sent, f_table in freq_matrix.items():
        idf_table = {}
        for word in f_table.keys():
            idf_table[word] = math.log10(total_sentences / float(sent_per_words[word]))
        idf_matrix[sent] = idf_table
    return idf_matrix


def tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}
    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
        tf_idf_table = {}
        for (word1, tf_value), (word2, idf_value) in zip(f_table1.items(), f_table2.items()):
            tf_idf_table[word1] = float(tf_value * idf_value)
        tf_idf_matrix[sent1] = tf_idf_table
    return tf_idf_matrix


def score_sentences(tf_idf_matrix):
    sentenceScore = {}
    for sent, f_table in tf_idf_matrix.items():
        total_score = sum(f_table.values())
        total_words = len(f_table)
        if total_words != 0:
            sentenceScore[sent] = total_score / total_words
    return sentenceScore


def average_score(sentence_score):
    return sum(sentence_score.values()) / len(sentence_score)


def create_summary(sentences, sentence_score, threshold):
    summary = ''
    for sentence in sentences:
        if sentence[:15] in sentence_score and sentence_score[sentence[:15]] >= threshold:
            summary += " " + sentence.text
    return summary


# GUI Application
class SummarizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Summarizer")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        layout = QVBoxLayout()

        # Input Type Selection
        self.input_type_combo = QComboBox()
        self.input_type_combo.addItems(["Manual Text", "Text File (.txt)", "PDF File (.pdf)", "Wikipedia URL"])
        layout.addWidget(QLabel("Select Input Type:"))
        layout.addWidget(self.input_type_combo)

        # Input Text Area
        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        # Summarize Button
        self.summarize_button = QPushButton("Summarize")
        self.summarize_button.clicked.connect(self.summarize_text)
        layout.addWidget(self.summarize_button)

        # Output Text Area
        self.output_text = QTextEdit()
        layout.addWidget(QLabel("Summary:"))
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def summarize_text(self):
        input_type = self.input_type_combo.currentText()
        text = ""

        if input_type == "Manual Text":
            text = self.input_text.toPlainText()
        elif input_type == "Text File (.txt)":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)")
            if file_path:
                text = file_text(file_path)
        elif input_type == "PDF File (.pdf)":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
            if file_path:
                text = pdfReader(file_path)
        elif input_type == "Wikipedia URL":
            url = self.input_text.toPlainText()
            text = wiki_text(url)

        if not text:
            QMessageBox.warning(self, "Error", "Failed to load input text.")
            return

        # Summarize the text
        doc = nlp(text)
        sentences = list(doc.sents)
        freq_matrix = frequency_matrix(sentences)
        tf_matrix_values = tf_matrix(freq_matrix)
        num_sent_per_words = sentences_per_words(freq_matrix)
        idf_matrix_values = idf_matrix(freq_matrix, num_sent_per_words, len(sentences))
        tf_idf_matrix_values = tf_idf_matrix(tf_matrix_values, idf_matrix_values)
        sentence_scores = score_sentences(tf_idf_matrix_values)
        threshold = average_score(sentence_scores)
        summary = create_summary(sentences, sentence_scores, 1.3 * threshold)

        # Display summary
        self.output_text.setPlainText(summary)


# Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SummarizerApp()
    window.show()
    sys.exit(app.exec_())
