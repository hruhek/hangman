# Hangman

A terminal-based Hangman game with ASCII art.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

```bash
uv sync
```

## Running the Game

```bash
uv run hangman
```

Or run directly:

```bash
uv run python src/hangman.py
```

## How to Play

1. A random word is selected
2. Guess one letter at a time
3. You have 6 wrong guesses before the hangman is complete
4. Win by guessing all letters in the word

## Credits

Created by [Amp](https://ampcode.com)
