"""Console Hangman game.

Usage:
    python hangman.py --words WORDS.txt --lives 6 --mode classic \
        --seed 231245 --hint off
"""

import argparse
import random

MIN_LIVES = 3
MAX_LIVES = 10


def parse_args():
    """Read and validate command-line parameters.

    Exits with code 2 (via argparse) on any invalid parameter.
    """
    parser = argparse.ArgumentParser(description="Console Hangman game.")
    parser.add_argument("--words", required=True,
                        help="path to a UTF-8 word list (one word per line)")
    parser.add_argument("--lives", type=int, default=6,
                        help="starting lives, between 3 and 10 (default 6)")
    parser.add_argument("--mode", choices=["classic", "hard"],
                        default="classic", help="rule set (default classic)")
    parser.add_argument("--seed", type=str, default=None,
                        help="randomness seed, e.g. your student ID")
    parser.add_argument("--hint", choices=["on", "off"], default="off",
                        help="hint system (default off)")

    args = parser.parse_args()

    if not MIN_LIVES <= args.lives <= MAX_LIVES:
        parser.error(f"--lives must be between {MIN_LIVES} and {MAX_LIVES}")

    return args

def load_words(path):
    """Load a list of words from a UTF-8 text file.

    Each line of the file should contain exactly one word. Leading and
    trailing whitespace is stripped. Empty lines are ignored.

    Returns:
        list of str: the words in the file, in the same order as they appear
    """
    words = []

    with open(path, encoding= "utf-8") as word_file:
        for line in word_file:
            word = line.strip()
            if len(word) >= 5 and word.isascii() and word.isalpha():
                words.append(word.upper())

    if not words:
        raise ValueError(f"No valid words found in {path}")
 
    return words

def choose_word(words, seed=None):
    """Choose a random word from a list of words.

    Args:
        words (list of str): the list of words to choose from"""
    generator = random.Random(seed)
    return generator.choice(words)



# GECICI TEST: Uye 5 main() fonksiyonunu yazinca bu iki satir silinecek.
if __name__ == "__main__":
    args = parse_args()
    words = load_words(args.words)
    word = choose_word(words, seed=args.seed)
    print(word)