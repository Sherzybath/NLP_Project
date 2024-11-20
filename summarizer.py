# summarizer.py

import sys
import math
import nltk
import spacy
from nltk.stem import WordNetLemmatizer


nltk.download('wordnet')

nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()

def summarize_text(text):
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
            tf_table = {}  #

            total_words_in_sentence = len(freq_table)
            for word, count in freq_table.items():
                tf_table[word] = count / total_words_in_sentence

            tf_matrix[sent] = tf_table

        return tf_matrix

    def sentences_per_words(freq_matrix):
        sent_per_words = {}

        for sent, f_table in freq_matrix.items():
            for word, count in f_table.items():
                if word in sent_per_words:
                    sent_per_words[word] += 1
                else:
                    sent_per_words[word] = 1

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

            # word1 and word2 are same
            for (word1, tf_value), (word2, idf_value) in zip(f_table1.items(), f_table2.items()):
                tf_idf_table[word1] = float(tf_value * idf_value)

            tf_idf_matrix[sent1] = tf_idf_table

        return tf_idf_matrix

    def score_sentences(tf_idf_matrix):
        sentenceScore = {}

        for sent, f_table in tf_idf_matrix.items():
            total_tfidf_score_per_sentence = 0

            total_words_in_sentence = len(f_table)
            for word, tf_idf_score in f_table.items():
                total_tfidf_score_per_sentence += tf_idf_score

            if total_words_in_sentence != 0:
                sentenceScore[sent] = total_tfidf_score_per_sentence / total_words_in_sentence

        return sentenceScore

    def average_score(sentence_score):
        total_score = 0
        for sent in sentence_score:
            total_score += sentence_score[sent]

        average_sent_score = (total_score / len(sentence_score))

        return average_sent_score

    def create_summary(sentences, sentence_score, threshold):
        summary = ''

        for sentence in sentences:
            if sentence[:15] in sentence_score and sentence_score[sentence[:15]] >= (threshold):
                summary += " " + sentence.text

        return summary

    # Converting received text into spaCy Doc object
    text = nlp(text)

    # Extracting all sentences from the text in a list
    sentences = list(text.sents)
    total_sentences = len(sentences)

    # Generating Frequency Matrix
    freq_matrix = frequency_matrix(sentences)

    # Generating Term Frequency Matrix
    tf_matrix = tf_matrix(freq_matrix)

    # Getting number of sentences containing a particular word
    num_sent_per_words = sentences_per_words(freq_matrix)

    # Generating ID Frequency Matrix
    idf_matrix = idf_matrix(freq_matrix, num_sent_per_words, total_sentences)

    # Generating Tf-Idf Matrix
    tf_idf_matrix = tf_idf_matrix(tf_matrix, idf_matrix)

    # Generating Sentence score for each sentence
    sentence_scores = score_sentences(tf_idf_matrix)

    # Setting threshold to average value (You are free to play with other values)
    threshold = average_score(sentence_scores)

    # Getting summary
    summary = create_summary(sentences, sentence_scores, 1.3 * threshold)

    return summary
