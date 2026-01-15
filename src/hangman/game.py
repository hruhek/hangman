import os
import random
from dataclasses import dataclass, field
from enum import Enum

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

MAX_WRONG_GUESSES = len(HANGMAN_STAGES) - 1


class GuessResult(Enum):
    INVALID = "invalid"
    ALREADY_GUESSED = "already_guessed"
    CORRECT = "correct"
    INCORRECT = "incorrect"


@dataclass
class GameState:
    word: str
    guessed_letters: set[str] = field(default_factory=set)
    wrong_guesses: int = 0
    message: str = ""

    @property
    def remaining_attempts(self) -> int:
        return MAX_WRONG_GUESSES - self.wrong_guesses

    def is_game_over(self) -> bool:
        return self.wrong_guesses >= MAX_WRONG_GUESSES

    def is_word_guessed(self) -> bool:
        return all(letter in self.guessed_letters for letter in self.word)


def get_random_word(words: list[str] | None = None) -> str:
    return random.choice(words or WORDS).lower()


def get_display_word(word: str, guessed_letters: set[str]) -> str:
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def validate_guess(guess: str) -> bool:
    return len(guess) == 1 and guess.isalpha()


def process_guess(state: GameState, guess: str) -> GuessResult:
    guess = guess.lower().strip()

    if not validate_guess(guess):
        state.message = "Please enter a single letter."
        return GuessResult.INVALID

    if guess in state.guessed_letters:
        state.message = "You already guessed that letter."
        return GuessResult.ALREADY_GUESSED

    state.guessed_letters.add(guess)

    if guess in state.word:
        state.message = f"✓ '{guess}' is in the word!"
        return GuessResult.CORRECT
    else:
        state.wrong_guesses += 1
        state.message = f"✗ '{guess}' is not in the word."
        return GuessResult.INCORRECT


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_game(state: GameState) -> None:
    clear_screen()
    print("🎮 HANGMAN")
    print(HANGMAN_STAGES[state.wrong_guesses])
    print(f"Word: {get_display_word(state.word, state.guessed_letters)}")
    print(f"Guessed: {', '.join(sorted(state.guessed_letters)) or 'None'}")
    print(f"Remaining attempts: {state.remaining_attempts}")

    if state.message:
        print(f"\n{state.message}")


def render_win(state: GameState) -> None:
    clear_screen()
    print("🎮 HANGMAN")
    print(HANGMAN_STAGES[state.wrong_guesses])
    print(f"Word: {get_display_word(state.word, state.guessed_letters)}")
    print(f"\n🎉 Congratulations! You won! The word was: {state.word}")


def render_loss(state: GameState) -> None:
    clear_screen()
    print("🎮 HANGMAN")
    print(HANGMAN_STAGES[state.wrong_guesses])
    print(f"\n💀 Game Over! The word was: {state.word}")


def play_game() -> None:
    state = GameState(word=get_random_word())

    while not state.is_game_over():
        render_game(state)
        guess = input("\nEnter a letter: ")
        process_guess(state, guess)

        if state.is_word_guessed():
            render_win(state)
            return

    render_loss(state)


def main() -> None:
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
