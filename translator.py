from transformers import MarianMTModel, MarianTokenizer

# Define models and tokenizers for Hindi-to-English and English-to-Hindi
hi_to_en_model_name = "Helsinki-NLP/opus-mt-hi-en"
en_to_hi_model_name = "Helsinki-NLP/opus-mt-en-hi"

# Load tokenizers and models
hi_to_en_tokenizer = MarianTokenizer.from_pretrained(hi_to_en_model_name)
hi_to_en_model = MarianMTModel.from_pretrained(hi_to_en_model_name)

en_to_hi_tokenizer = MarianTokenizer.from_pretrained(en_to_hi_model_name)
en_to_hi_model = MarianMTModel.from_pretrained(en_to_hi_model_name)

# Functions for translation
def translate_hindi_to_english(sentence):
    inputs = hi_to_en_tokenizer.encode(sentence, return_tensors="pt")
    translated = hi_to_en_model.generate(inputs)
    return hi_to_en_tokenizer.decode(translated[0], skip_special_tokens=True)

def translate_english_to_hindi(sentence):
    inputs = en_to_hi_tokenizer.encode(sentence, return_tensors="pt")
    translated = en_to_hi_model.generate(inputs)
    return en_to_hi_tokenizer.decode(translated[0], skip_special_tokens=True)

