import tempfile
from pathlib import Path
from anki_generator_app.downloader import get_webpage_content, download_file
from anki_generator_app.genanki_handler import GenankiVocabHandler
from anki_generator_app.dictionaries import get_dictionary_handler


class AnkiGenerator:
    """
    Anki generator, example of usage:

    anki_output_file_path = Path("tests/data/my_deck.apkg")
    anki_generator = AnkiGenerator("TestDeck")
    anki_generator.add_word("prudent")
    anki_generator.add_word("deride")
    anki_generator.generate_flashcards(anki_output_file_path)
    """

    def __init__(self, deck_name: str, dictionary: str = "Cambridge"):
        self.dictionary = get_dictionary_handler(dictionary)
        self.anki_handler = GenankiVocabHandler(deck_name)
        self.words = []

    def add_word(self, word: str):
        self.words.append(word)

    def add_words_from_txt_file(self, path_to_file: Path):
        with open(path_to_file) as file:
            for line in file.readlines():
                self.add_word(line.lower().strip())

    def generate_flashcards(self, output_file: Path):
        with tempfile.TemporaryDirectory() as temp_dir:
            for word in self.words:
                word_webpage = get_webpage_content(self.dictionary.get_word_url(word))
                meanings = self.dictionary.get_word_meanings(word_webpage)
                ipa = self.dictionary.get_ipa(word_webpage)
                examples_of_usage = self.dictionary.get_word_examples_of_usage(
                    word_webpage
                )
                media_file_name = f"{word}.mp3"
                mp3_media_file_path = Path(temp_dir) / media_file_name
                mp3_media_url = self.dictionary.get_word_us_pronunciation_url(
                    word_webpage
                )
                download_file(mp3_media_url, mp3_media_file_path)
                self.anki_handler.add_vocab_flashcard_to_deck(
                    mp3_media_file_path,
                    word,
                    meanings,
                    examples_of_usage,
                    ipa,
                    media_file_name,
                )
            self.anki_handler.save_apkg_anki_file(output_file)


if __name__ == "__main__":
    words = ["person", "use"]
    anki_output_file_path = Path("tests/data/prudent.apkg")
    anki_generator = AnkiGenerator("TestDeck")
    anki_generator.add_word("prudent")
    anki_generator.generate_flashcards(anki_output_file_path)
