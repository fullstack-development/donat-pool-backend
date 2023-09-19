from better_profanity import Profanity
from better_profanity.varying_string import VaryingString
from better_profanity.utils import (
    read_wordlist,
    get_complete_path_of_file,
    )
from itertools import chain
from collections.abc import Iterable
from better_profanity.constants import ALLOWED_CHARACTERS


class DonatPoolModerator(Profanity):
    def __init__(self, additional_words):       
        self.CENSOR_WORDSET = []
        self.CHARS_MAPPING = {
            "a": ("a", "@", "*", "4"),
            "i": ("i", "*", "l", "1"),
            "o": ("o", "*", "0", "@"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "l": ("l", "1"),
            "e": ("e", "*", "3"),
            "s": ("s", "$", "5"),
            "t": ("t", "7"),
        }
        self.MAX_NUMBER_COMBINATIONS = 1
        self.ALLOWED_CHARACTERS = ALLOWED_CHARACTERS
        self._default_wordlist_filename = get_complete_path_of_file(
            "profanity_wordlist.txt"
        )

        self.load_all_censor_words(additional_words)
    
    def load_all_censor_words(self, additional_words, **kwargs):
        words = read_wordlist(self._default_wordlist_filename)
        all_words = chain(words, additional_words)
        self._populate_words_to_wordset(all_words, **kwargs)

def is_text_acceptable(additional_words, moderating_text):
    profanity = DonatPoolModerator(additional_words)
    return not profanity.contains_profanity(moderating_text)
