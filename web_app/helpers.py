import logging
from pathlib import Path
from anki_generator_app.anki_generator import AnkiGenerator


def parse_text_file_to_words(file_path: Path) -> [str]:
    """

    :param file_path:
    :return: list of words
    """
    with open(file_path) as file:
        content = file.read()
    if "," in content:
        return [word.strip() for word in content.split(",") if word.strip()]

    return [word.strip() for word in content.split("\n") if word.strip()]


def generate_anki(deck_name, words, output_file):
    anki_generator = AnkiGenerator(deck_name)
    for word in words:
        logging.info(f"Adding word {word} to the anki deck")
        anki_generator.add_word(word)
    problematic_words = anki_generator.generate_flashcards(output_file)
    return problematic_words
