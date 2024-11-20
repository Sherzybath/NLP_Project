# from utils.tokenizer import initialize_model
from utils import initialize_model


class Paraphraser:
    def __init__(self):
        # Initialize model, tokenizer, and device (GPU or CPU)
        self.tokenizer, self.model, self.device = initialize_model()

    def get_response(self, input_text, num_return_sequences=1):
        # Tokenize and generate paraphrased response
        batch = self.tokenizer.prepare_seq2seq_batch(
            [input_text], truncation=True, padding="longest", max_length=60, return_tensors="pt"
        ).to(self.device)

        translated = self.model.generate(
            **batch, max_length=60, num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5
        )
        # Decode and return the paraphrased text
        return self.tokenizer.batch_decode(translated, skip_special_tokens=True)

    def paraphrase_text(self, context):
        # Split context into sentences and paraphrase each sentence
        sentences = context.split(". ")
        paraphrased_sentences = [self.get_response(sentence, 1)[0] for sentence in sentences]
        # Join paraphrased sentences and return the result
        return " ".join(paraphrased_sentences)
