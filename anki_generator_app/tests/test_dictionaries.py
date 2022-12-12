import pytest
from pathlib import Path
from anki_generator_app.dictionaries import get_dictionary_handler, CambridgeDictionary
from .data.words_meanings import prudent_meanings


@pytest.mark.parametrize(
    "word_html_file_path, expected_meanings",
    [
        (Path("tests/data/prudent.html"), prudent_meanings),
    ],
)
def test_proper_dict_handler_is_used_andword_meanings_are_properly_parsed(
    word_html_file_path, expected_meanings
):
    dictionary = "cambridge"
    cambridge_dict = get_dictionary_handler(dictionary)

    with open(word_html_file_path) as prudent_cb_page_content:
        meanings = cambridge_dict.get_word_meanings(prudent_cb_page_content.read())

    assert type(cambridge_dict) == CambridgeDictionary
    assert meanings == expected_meanings
