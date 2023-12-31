import unicodedata as ud
from collections import defaultdict
from collections import Counter


class AlphabetDetector:
    def __init__(self, no_memory=False):
        self.alphabet_letters = defaultdict(dict)
        self.no_memory = no_memory

    def is_in_alphabet(self, uchr, alphabet):
        if self.no_memory:
            return alphabet in ud.name(uchr)
        try:
            return self.alphabet_letters[alphabet][uchr]
        except KeyError:
            return self.alphabet_letters[alphabet].setdefault(
                uchr, alphabet in ud.name(uchr))

    def only_alphabet_chars(self, unistr, alphabet):
        return all(self.is_in_alphabet(uchr, alphabet)
                   for uchr in unistr if uchr.isalpha())

    def ud_name(self, char):
        try:
            name = ud.name(char)
        except:
            with open('log.txt', 'a') as f:
                f.write('char: ' + str(char) + '\n')
            return 'N/A'
        if ' ' in name:
            return name.split(' ')[0]
        print(name)
        return name

    def detect_alphabet(self, unistr):
        return set(self.ud_name(char) for char in unistr if char.isalpha())

    def is_greek(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'GREEK') else False

    def is_cyrillic(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'CYRILLIC') else False

    def is_latin(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'LATIN') else False

    def is_arabic(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'ARABIC') else False

    def is_hebrew(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'HEBREW') else False

    # NOTE: this only detects Chinese script characters (Hanzi/Kanji/Hanja).
    # it does not detect other CJK script characters like Hangul or Katakana
    def is_cjk(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'CJK') else False

    def is_hangul(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'HANGUL') else False

    def is_hiragana(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'HIRAGANA') else False

    def is_katakana(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'KATAKANA') else False

    def is_thai(self, unistr):
        return True if self.only_alphabet_chars(unistr, 'THAI') else False


detector = AlphabetDetector()


def get_alphabets(list_of_texts: list):
    result = []
    for item in list_of_texts:
        result.extend(list(detector.detect_alphabet(item)))
    return Counter(result)
