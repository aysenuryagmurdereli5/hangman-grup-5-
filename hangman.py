"""Console Hangman game.

Usage:
    python hangman.py --words WORDS.txt --lives 6 --mode classic \
        --seed 231245 --hint off
"""

import argparse
import random
import string
import sys

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

    with open(path, encoding="utf-8") as word_file:
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
        words (list of str): the list of words to choose from
        seed (str | None): optional seed for deterministic selection"""
    generator = random.Random(seed)
    return generator.choice(words)


def show_state(word, guessed, lives):
    """Display the masked word, remaining lives, and guessed letters."""
    masked_word = " ".join(
        letter if letter in guessed else "_" for letter in word
    )
    guessed_display = ", ".join(sorted(guessed)) if guessed else "-"

    print(f"Word: {masked_word}")
    print(f"Lives: {lives}")
    print(f"Guessed: {guessed_display}")


def read_input(hint_enabled):
    """Prompt the user for a single A-Z letter or '?' if hints are enabled."""
    while True:
        raw_input = input("> Enter a letter: ").strip()

        if raw_input == "?":
            if hint_enabled:
                return "?"
            print("Hints are disabled. Please enter a single A-Z letter.")
            continue

        if (len(raw_input) == 1 and raw_input.isascii()
                and raw_input.isalpha()):
            return raw_input.upper()

        print("Invalid input. Please enter a single A-Z letter.")


def show_hint_message(revealed_letter):
    """Display the hint reveal message."""
    print(f"[HINT] Revealed: {revealed_letter.lower()} (life -1)")


def show_repeat_message(letter):
    """Display a warning when a letter has already been guessed."""
    print(f"You already guessed '{letter}'. Try another letter.")


def show_game_result(won, word):
    """Display the final win or game over message."""
    if won:
        print(f"Congratulations! Word: {word}")
    else:
        print(f"Game over. Word: {word}")


# Oyuncunun bir harf tahminini işler.
def apply_guess(word, guessed_letters, lives, letter, mode):
    """Return the remaining lives and the guess result."""

    # Yeni harf önceki tahminler arasında mı?
    if letter in guessed_letters:
        # Tekrar tahminde canı olduğu gibi bırak ve sonucu döndür.
        return lives, "repeat"

        # Bu harf ilk kez girildiği için tahminler kümesine ekle.
    guessed_letters.add(letter)

    # Harf gizli kelimenin içinde mi?
    if letter in word:
        # Doğru tahminde canı değiştirme ve sonucu döndür.
        return lives, "correct"

        # Yanlış tahminin normal cezası 1 can.
    penalty = 1

    # Hard modda yanlış tahmin edilen harf sesliyse ceza 2 can.
    if mode == "hard" and letter in "AEIOU":
        penalty = 2

    # Cezayı düş, ama canın sıfırın altına inmesini önle.
    remaining_lives = max(0, lives - penalty)

    # Kalan canı ve yanlış tahmin sonucunu döndür.
    return remaining_lives, "wrong"


def apply_hint(word, guessed_letters, lives):
    """Reveal the first hidden letter and return the new lives and letter."""

    # Kelimeyi soldan sağa, harf harf dolaş.
    for letter in word:
        # Tahminler kümesinde olmayan harf hâlâ gizlidir.
        if letter not in guessed_letters:
            # Harfi kümeye ekle. Ekran bu harfin tüm tekrarlarını açar.
            guessed_letters.add(letter)

            # İpucu 1 can götürür. Can sıfırın altına inmez.
            remaining_lives = max(0, lives - 1)

            # Canı ve açılan harfi döndür. Böylece tek ipucunda dururuz.
            return remaining_lives, letter

    # Gizli harf kalmadıysa canı değiştirme. None, harf açılmadığını belirtir.
    return lives, None


def has_won(word, guessed_letters):
    """Return whether every letter in the word has been revealed."""

    # Gizli kelimenin harflerini sırayla kontrol et.
    for letter in word:
        # Bir harf bile açılmadıysa oyuncu henüz kazanmadı.
        if letter not in guessed_letters:
            return False

    # Döngü bittiğinde bütün harfler kontrol edilmiş ve açılmıştır.
    return True


def play_game(args, word):
    """Run the main game loop and return the exit code."""
    guessed = set()
    lives = args.lives
    hint_enabled = args.hint == "on"

    while lives > 0 and not has_won(word, guessed):
        show_state(word, guessed, lives)
        user_input = read_input(hint_enabled)

        if user_input == "?":
            lives, revealed = apply_hint(word, guessed, lives)
            if revealed is not None:
                show_hint_message(revealed)
        else:
            lives, result = apply_guess(
                word, guessed, lives, user_input, args.mode
            )
            if result == "repeat":
                show_repeat_message(user_input)

    won = has_won(word, guessed)
    show_game_result(won, word)
    return 0


def main():
    """Connect all game components, handle errors, and exit cleanly."""
    try:
        args = parse_args()
        words = load_words(args.words)
        word = choose_word(words, seed=args.seed)
        exit_code = play_game(args, word)
        sys.exit(exit_code)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
