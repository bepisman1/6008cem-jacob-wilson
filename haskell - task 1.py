import os
import nltk
from nltk.util import ngrams
nltk.download('punkt')
from collections import defaultdict
import random
import pickle

# Define file paths
corpus_file_path = "corpus.txt"
model_file_path = "language_model.pkl"

# List of non-fiction books from Project Gutenberg
book_paths = [
    "D:\Downlaods\pg73324.txt",
    "D:\Downlaods\pg73325.txt",
    # Add more books here
]

def create_corpus(book_paths, corpus_file_path):
    with open(corpus_file_path, "w", encoding="utf-8") as corpus_file:
        for book_path in book_paths:
            with open(book_path, "r", encoding="utf-8") as book_file:
                corpus_file.write(book_file.read())

def zero():
    return 0

def default_zero():
    return defaultdict(zero)

def build_ngram_model(corpus, n):
    ngram_model = defaultdict(default_zero)
    tokens = nltk.word_tokenize(corpus)
    for i in range(len(tokens) - n + 1):
        ngram_tuple = tuple(tokens[i:i+n])
        context = ngram_tuple[:-1]
        word = ngram_tuple[-1]
        ngram_model[context][word] += 1
    return ngram_model



def generate_text(model, seed=None, max_length=100):
    if seed is None:
        seed = random.choice(list(model.keys()))
    text = list(seed)
    context = seed
    while len(text) < max_length:
        if context not in model:
            break
        possible_next_words = list(model[context].keys())
        probabilities = list(model[context].values())
        next_word = random.choices(possible_next_words, weights=probabilities)[0]
        text.append(next_word)
        context = tuple(text[-n:])
    return " ".join(text)

def main():
    if not os.path.exists(corpus_file_path):
        create_corpus(book_paths, corpus_file_path)

    # Load the corpus
    with open(corpus_file_path, "r", encoding="utf-8") as corpus_file:
        corpus_text = corpus_file.read()

    # Build the n-gram model
    n = 2  # Change n as desired
    ngram_model = build_ngram_model(corpus_text, n)

    # Persist the language model to disk
    with open(model_file_path, "wb") as model_file:
        pickle.dump(dict(ngram_model), model_file)

    # Generate sample text
    generated_text = generate_text(ngram_model)
    print(generated_text)

if __name__ == "__main__":
    main()