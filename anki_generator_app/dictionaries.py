"""
Currently only supported dictionary is the English Cambridge dictionary
https://dictionary.cambridge.org/english
"""
import abc
import re
from bs4 import BeautifulSoup


class Dictionary(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_word_meanings(word_page_content: str) -> [str]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_examples_of_usage(word_page_content: str) -> [str]:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_url(word_page_content: str) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_us_pronunciation_url(word_page_content: str) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_ipa(word_page_content: str) -> str:
        pass


class CambridgeDictionary(Dictionary):
    MAIN_URL = "https://dictionary.cambridge.org/"
    WORD_URL = "https://dictionary.cambridge.org/dictionary/english/{word}"
    PRONUNCIATION_URL = "https://dictionary.cambridge.org/{audio_src}"

    BEAUTIFUL_SOUP_MEANING_DIV = "div", {"class": "def ddef_d db"}
    BEAUTIFUL_SOUP_EXAMPLE_DIV = "div", {"class": "examp dexamp"}
    BEAUTIFUL_SOUP_PRONUNCIATION_ELEMENT = "source", {"type": "audio/mpeg"}
    BEAUTIFUL_SOUP_IPA_ELEMENT = "span", {"class": "ipa dipa lpr-2 lpl-1"}

    MEANING_REGEXP = re.compile(r">(\w+?)<(?!\/s)|>(.*?)<")
    EXAMPLE_REGEXP = re.compile(r">(\w+?)<(?!\/s)|>(.*?)<")
    IPA_REGEXP = re.compile(r">(.*?)<")

    PRONUNCIATION_REGEXP = re.compile(r"")

    @staticmethod
    def get_word_meanings(word_page_content: str) -> [str]:
        meaning_page_elements = BeautifulSoup(
            word_page_content, "html.parser"
        ).find_all(*CambridgeDictionary.BEAUTIFUL_SOUP_MEANING_DIV)

        meanings_regexp_groups = CambridgeDictionary._get_all_meaning_regexp_groups(
            meaning_page_elements
        )
        return CambridgeDictionary._join_and_return_all_meanings_from_regexp_groups(
            meanings_regexp_groups
        )

    @staticmethod
    def get_word_examples_of_usage(word_page_content: str) -> [str]:
        examples_page_elements = BeautifulSoup(
            word_page_content, "html.parser"
        ).find_all(*CambridgeDictionary.BEAUTIFUL_SOUP_EXAMPLE_DIV)
        examples_regexp_groups = CambridgeDictionary._get_all_examples_regexp_groups(
            examples_page_elements
        )
        return CambridgeDictionary._join_and_return_all_examples_from_regexp_groups(
            examples_regexp_groups
        )

    @staticmethod
    def get_word_url(word: str) -> str:
        return CambridgeDictionary.WORD_URL.format(word=word)

    @staticmethod
    def get_word_us_pronunciation_url(word_page_content: str) -> str:
        us_pronunciation = None
        pronunciation_elements = BeautifulSoup(
            word_page_content, "html.parser"
        ).find_all(CambridgeDictionary.BEAUTIFUL_SOUP_PRONUNCIATION_ELEMENT)
        for element in pronunciation_elements:
            if "us_pron" in str(element) and "mp3" in str(element):
                us_pronunciation = str(element)
                break
        return (
            CambridgeDictionary.PRONUNCIATION_URL.format(
                audio_src=us_pronunciation[
                    us_pronunciation.find('"') + 1: us_pronunciation.find(".mp3") + 4
                ]
            )
            if us_pronunciation
            else None
        )

    @staticmethod
    def get_ipa(word_page_content: str) -> str:
        ipa_elements = BeautifulSoup(word_page_content, "html.parser").find_all(
            *CambridgeDictionary.BEAUTIFUL_SOUP_IPA_ELEMENT
        )
        ipa_all_regexp_groups = CambridgeDictionary._get_all_ipa_regexp_groups(
            ipa_elements
        )
        if ipa_all_regexp_groups:
            return (
                "".join(ipa_all_regexp_groups[1])
                if len(ipa_all_regexp_groups) > 1
                else "".join(ipa_all_regexp_groups[0])
            )
        return ""

    @staticmethod
    def _get_all_ipa_regexp_groups(ipa_page_elements: []) -> [(str, str)]:
        return [
            re.findall(CambridgeDictionary.IPA_REGEXP, str(element))
            for element in ipa_page_elements
        ]

    @staticmethod
    def _get_all_meaning_regexp_groups(meaning_page_elements: []) -> [(str, str)]:
        return [
            re.findall(CambridgeDictionary.MEANING_REGEXP, str(element))
            for element in meaning_page_elements
        ]

    @staticmethod
    def _join_and_return_all_meanings_from_regexp_groups(
        meaning_regexp_groups: [(str, str)]
    ) -> [str]:
        return [
            ("".join((map(lambda x: x[0] + x[1], meaning))))
            for meaning in meaning_regexp_groups
        ]

    @staticmethod
    def _get_all_examples_regexp_groups(meaning_page_elements: []) -> [(str, str)]:
        return [
            re.findall(CambridgeDictionary.EXAMPLE_REGEXP, str(element))
            for element in meaning_page_elements
        ]

    @staticmethod
    def _join_and_return_all_examples_from_regexp_groups(
        meaning_regexp_groups: [(str, str)]
    ) -> [str]:
        return [
            ("".join((map(lambda x: x[0] + x[1], meaning))))
            for meaning in meaning_regexp_groups
        ]


def get_dictionary_handler(dictionary: str) -> Dictionary:
    supported_dictionaries = {"cambridge": CambridgeDictionary}

    dictionary = dictionary.lower()
    if dictionary in supported_dictionaries:
        return supported_dictionaries[dictionary]()
    raise DictionaryNotSupportedError(
        f"This dictionary is not supported: {dictionary}, "
        f"supported dictionaries: {supported_dictionaries.keys}"
    )


class DictionaryNotSupportedError(Exception):
    pass
