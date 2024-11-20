 
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def initialize_model():
    model_name = "tuner007/pegasus_paraphrase"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    return tokenizer, model, device
