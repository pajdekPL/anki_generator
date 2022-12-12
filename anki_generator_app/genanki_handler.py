import genanki
from pathlib import Path
from random import randint


class GenankiVocabHandler:
    MODEL_ID = int(f"1091735{randint(100, 999)}")
    DECK_ID = int(f"2059400{randint(100, 999)}")
    MODELS = {
        "vocab_simple_model": genanki.Model(
            MODEL_ID,
            "Simple Model with Media",
            fields=[
                {"name": "Word"},
                {"name": "Sound"},
                {"name": "Meaning"},
                {"name": "Examples"},
                {"name": "IPA"},
            ],
            templates=[
                {
                    "name": "{{Word}}",
                    "qfmt": "{{Word}}<br>{{Sound}}",
                    "afmt": "{{Meaning}}<hr>{{Examples}}<hr>{{IPA}}",
                },
            ],
        )
    }

    def __init__(self, deck_name: str, model: str = "vocab_simple_model") -> None:
        self.deck_name = deck_name
        if model in GenankiVocabHandler.MODELS:
            self.model = GenankiVocabHandler.MODELS[model]
        else:
            raise ErrorModelDoesNotExist(
                f"Model: {model} does not exist, available models: "
                f"{GenankiVocabHandler.MODELS.keys()}"
            )

        self.deck = genanki.Deck(GenankiVocabHandler.DECK_ID, self.deck_name)
        self.package = genanki.Package(self.deck)
        self.package.media_files = []

    def add_media_file(self, file_path: Path):
        self.package.media_files.append(file_path)

    def add_note_vocab_simple_model(
        self,
        word: str,
        meanings: [str],
        examples: [str],
        ipa: [str],
        pronunciation_mp3: [str],
    ) -> None:
        new_note = genanki.Note(
            model=self.model,
            fields=[
                word,
                f"[sound:{pronunciation_mp3}]",
                "<br>".join(meanings),
                "<br>".join(examples),
                ipa,
            ],
        )
        self.deck.add_note(new_note)

    def add_vocab_flashcard_to_deck(
        self,
        media_file_path: Path,
        word: str,
        meanings: [str],
        examples: [str],
        ipa: [str],
        media_file_name: [str],
    ) -> None:
        self.add_media_file(media_file_path)
        self.add_note_vocab_simple_model(word, meanings, examples, ipa, media_file_name)

    def save_apkg_anki_file(self, path: Path) -> Path:
        self.package.write_to_file(path)
        return path


class ErrorModelDoesNotExist(Exception):
    pass
