import os
from pathlib import Path
from unittest.mock import patch, call
from pytest import fixture
from anki_generator_app.anki_generator import AnkiGenerator
import tempfile


def test_anki_flashcard_is_properly_generated_for_word_prudent(mocked_requests):
    data_path = Path(os.path.dirname(os.path.realpath(__file__))) / "data"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/51.0.2704.103 Safari/537.36"
    }
    deck_name = "TestDeck"
    expected_apkg_file_size = 57
    word = "prudent"
    requests_get_expected_calls = [
        call(
            "https://dictionary.cambridge.org/dictionary/english/prudent",
            headers=headers,
        ),
        call(
            "https://dictionary.cambridge.org//media/english/us_pron/p/pru/prude/prudent.mp3",
            headers=headers,
        ),
    ]

    class WordWebPageContent:
        web_page_for_word = data_path / "prudent.html"
        content = web_page_for_word.read_text()
        status_code = 200

    class PrudentMp3:
        prudent_mp3_file = data_path / "prudent.mp3"
        content = prudent_mp3_file.read_bytes()

    mocked_requests.get.side_effect = [WordWebPageContent, PrudentMp3]

    with tempfile.NamedTemporaryFile() as file:
        output_file = Path(file.name)
        anki_generator = AnkiGenerator(deck_name)
        anki_generator.add_word(word)
        anki_generator.generate_flashcards(output_file)
        assert int(os.stat(output_file).st_size / 1024) == expected_apkg_file_size
    mocked_requests.get.assert_has_calls(requests_get_expected_calls, any_order=False)


@fixture()
def mocked_requests():
    with patch("anki_generator_app.downloader.requests") as mock_requests:
        yield mock_requests
