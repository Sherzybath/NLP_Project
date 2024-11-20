 
import unittest
from paraphraser.paraphrase import Paraphraser

class TestParaphraser(unittest.TestCase):
    def test_paraphrase_text(self):
        paraphraser = Paraphraser()
        input_text = "This is a test sentence."
        result = paraphraser.paraphrase_text(input_text)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, input_text)

if __name__ == "__main__":
    unittest.main()
