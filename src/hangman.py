import os
import random


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


WORDS = [
    "python",
    "programming",
    "hangman",
    "developer",
    "keyboard",
    "computer",
    "algorithm",
    "function",
    "variable",
    "terminal",
]

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    """,
]


def get_display_word(word: str, guessed_letters: set[str]) -> str:
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def play_game() -> None:
    word = random.choice(WORDS).lower()
    guessed_letters: set[str] = set()
    wrong_guesses = 0
    max_wrong = len(HANGMAN_STAGES) - 1
    message = ""

    while wrong_guesses < max_wrong:
        clear_screen()
        print("🎮 HANGMAN")
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"Word: {get_display_word(word, guessed_letters)}")
        print(f"Guessed: {', '.join(sorted(guessed_letters)) or 'None'}")
        print(f"Remaining attempts: {max_wrong - wrong_guesses}")

        if message:
            print(f"\n{message}")

        guess = input("\nEnter a letter: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            message = "Please enter a single letter."
            continue

        if guess in guessed_letters:
            message = "You already guessed that letter."
            continue

        guessed_letters.add(guess)

        if guess in word:
            message = f"✓ '{guess}' is in the word!"
            if all(letter in guessed_letters for letter in word):
                clear_screen()
                print("🎮 HANGMAN")
                print(HANGMAN_STAGES[wrong_guesses])
                print(f"Word: {get_display_word(word, guessed_letters)}")
                print(f"\n🎉 Congratulations! You won! The word was: {word}")
                return
        else:
            wrong_guesses += 1
            message = f"✗ '{guess}' is not in the word."

    clear_screen()
    print("🎮 HANGMAN")
    print(HANGMAN_STAGES[wrong_guesses])
    print(f"\n💀 Game Over! The word was: {word}")


def main() -> None:
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
