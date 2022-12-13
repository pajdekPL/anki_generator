import os
from pathlib import Path
from unittest.mock import patch, call
from pytest import fixture
from web_app.helpers import parse_text_file_to_words, generate_anki

data_path = Path(os.path.dirname(os.path.realpath(__file__))) / "data"


def test_parsing_user_input_for_separated_words_by_commas():
    expected_parsed_words = ["prudent", "social", "person", "ring", "car", "sport"]
    words_separated_by_commas_file = data_path / "words_separated_by_commas.txt"

    assert (
        parse_text_file_to_words(words_separated_by_commas_file)
        == expected_parsed_words
    )


def test_parsing_user_input_for_separated_words_by_newlines():
    expected_parsed_words = ["prudent", "social", "person", "ring", "car", "sport"]
    words_separated_by_commas_file = data_path / "words_separated_by_newlines.txt"

    assert (
        parse_text_file_to_words(words_separated_by_commas_file)
        == expected_parsed_words
    )


def test_generate_anki_flash_cards(mocked_anki_generator):
    words = ["proud", "game", "innocent"]
    expected_add_word_calls = [call("proud"), call("game"), call("innocent")]
    mock_deck_name = "mocked_deck"
    mock_file = Path("monkey_path")

    generate_anki(mock_deck_name, words, mock_file)

    mocked_anki_generator.assert_called_once_with(mock_deck_name)
    mocked_anki_generator().add_word.assert_has_calls(expected_add_word_calls)
    mocked_anki_generator().generate_flashcards.assert_called_once_with(mock_file)


@fixture()
def mocked_anki_generator():
    with patch("web_app.helpers.AnkiGenerator") as mock_anki_generator:
        yield mock_anki_generator
