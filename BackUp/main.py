 
from paraphraser.paraphrase import Paraphraser

if __name__ == "__main__":
    # Prompt user input
    user_input = input("Enter text to paraphrase: ")

    # Initialize Paraphraser
    paraphraser = Paraphraser()
    
    # Get paraphrased text
    result = paraphraser.paraphrase_text(user_input)
    
    # Print original and paraphrased text
    print(f"Original: {user_input}")
    print(f"Paraphrased: {result}")
