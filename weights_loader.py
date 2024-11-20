import os
import pickle

from model import Encoder, Decoder
encoder = Encoder(vocab_size, embedding_dim, units, batch_size)
decoder = Decoder(vocab_size, embedding_dim, units, batch_size)

# Load the weights
encoder.load_weights(os.path.join(save_path, "encoder_weights.h5"))
decoder.load_weights(os.path.join(save_path, "decoder_weights.h5"))

# Load the tokenizer (if used)
with open(os.path.join(save_path, "tokenizer.pkl"), "rb") as f:
    tokenizer = pickle.load(f)