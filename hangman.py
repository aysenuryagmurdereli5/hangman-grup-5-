"""Console Hangman game.

Usage:
    python hangman.py --words WORDS.txt --lives 6 --mode classic \
        --seed 231245 --hint off
"""

import argparse

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






# GECICI TEST: Uye 5 main() fonksiyonunu yazinca bu iki satir silinecek.
if __name__ == "__main__":
    print(parse_args())