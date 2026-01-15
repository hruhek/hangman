from hangman import (
    GameState,
    GuessResult,
    get_display_word,
    get_random_word,
    process_guess,
    validate_guess,
    WORDS,
)


class TestGetDisplayWord:
    def test_no_letters_guessed(self):
        assert get_display_word("python", set()) == "_ _ _ _ _ _"

    def test_some_letters_guessed(self):
        assert get_display_word("python", {"p", "t"}) == "p _ t _ _ _"

    def test_all_letters_guessed(self):
        assert get_display_word("cat", {"c", "a", "t"}) == "c a t"

    def test_extra_letters_guessed(self):
        assert get_display_word("hi", {"h", "i", "x", "z"}) == "h i"

    def test_empty_word(self):
        assert get_display_word("", set()) == ""


class TestValidateGuess:
    def test_valid_single_letter(self):
        assert validate_guess("a") is True
        assert validate_guess("Z") is True

    def test_invalid_empty_string(self):
        assert validate_guess("") is False

    def test_invalid_multiple_letters(self):
        assert validate_guess("ab") is False

    def test_invalid_number(self):
        assert validate_guess("1") is False

    def test_invalid_special_character(self):
        assert validate_guess("!") is False

    def test_invalid_space(self):
        assert validate_guess(" ") is False


class TestGetRandomWord:
    def test_returns_word_from_default_list(self):
        word = get_random_word()
        assert word in WORDS

    def test_returns_word_from_custom_list(self):
        custom_words = ["apple", "banana"]
        word = get_random_word(custom_words)
        assert word in custom_words

    def test_returns_lowercase(self):
        word = get_random_word(["UPPER", "MiXeD"])
        assert word == word.lower()


class TestGameState:
    def test_initial_state(self):
        state = GameState(word="test")
        assert state.word == "test"
        assert state.guessed_letters == set()
        assert state.wrong_guesses == 0
        assert state.message == ""

    def test_remaining_attempts(self):
        state = GameState(word="test")
        assert state.remaining_attempts == 6
        state.wrong_guesses = 3
        assert state.remaining_attempts == 3

    def test_is_game_over_false(self):
        state = GameState(word="test", wrong_guesses=5)
        assert state.is_game_over() is False

    def test_is_game_over_true(self):
        state = GameState(word="test", wrong_guesses=6)
        assert state.is_game_over() is True

    def test_is_word_guessed_false(self):
        state = GameState(word="cat", guessed_letters={"c", "a"})
        assert state.is_word_guessed() is False

    def test_is_word_guessed_true(self):
        state = GameState(word="cat", guessed_letters={"c", "a", "t"})
        assert state.is_word_guessed() is True

    def test_is_word_guessed_with_extra_letters(self):
        state = GameState(word="cat", guessed_letters={"c", "a", "t", "x", "z"})
        assert state.is_word_guessed() is True


class TestProcessGuess:
    def test_invalid_guess_empty(self):
        state = GameState(word="test")
        result = process_guess(state, "")
        assert result == GuessResult.INVALID
        assert state.wrong_guesses == 0
        assert len(state.guessed_letters) == 0

    def test_invalid_guess_multiple_chars(self):
        state = GameState(word="test")
        result = process_guess(state, "ab")
        assert result == GuessResult.INVALID

    def test_invalid_guess_number(self):
        state = GameState(word="test")
        result = process_guess(state, "5")
        assert result == GuessResult.INVALID

    def test_already_guessed(self):
        state = GameState(word="test", guessed_letters={"t"})
        result = process_guess(state, "t")
        assert result == GuessResult.ALREADY_GUESSED
        assert state.wrong_guesses == 0

    def test_correct_guess(self):
        state = GameState(word="test")
        result = process_guess(state, "t")
        assert result == GuessResult.CORRECT
        assert "t" in state.guessed_letters
        assert state.wrong_guesses == 0

    def test_incorrect_guess(self):
        state = GameState(word="test")
        result = process_guess(state, "x")
        assert result == GuessResult.INCORRECT
        assert "x" in state.guessed_letters
        assert state.wrong_guesses == 1

    def test_guess_case_insensitive(self):
        state = GameState(word="test")
        result = process_guess(state, "T")
        assert result == GuessResult.CORRECT
        assert "t" in state.guessed_letters

    def test_guess_strips_whitespace(self):
        state = GameState(word="test")
        result = process_guess(state, " t ")
        assert result == GuessResult.CORRECT
        assert "t" in state.guessed_letters

    def test_message_set_on_correct(self):
        state = GameState(word="test")
        process_guess(state, "t")
        assert "✓" in state.message
        assert "'t'" in state.message

    def test_message_set_on_incorrect(self):
        state = GameState(word="test")
        process_guess(state, "x")
        assert "✗" in state.message
        assert "'x'" in state.message
