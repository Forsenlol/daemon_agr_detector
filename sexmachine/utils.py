## Transliterate
# https://github.com/opendatakosovo/cyrillic-transliteration/blob/master/cyrtranslit/__init__.py

import copy
import sys

# Build the dictionaries to transliterate Serbian cyrillic to latin and vice versa.

# This dictionary is to transliterate from cyrillic to latin.
SR_CYR_TO_LAT_DICT = {
    u'А': u'A', u'а': u'a',
    u'Б': u'B', u'б': u'b',
    u'В': u'V', u'в': u'v',
    u'Г': u'G', u'г': u'g',
    u'Д': u'D', u'д': u'd',
    u'Ђ': u'Đ', u'ђ': u'đ',
    u'Е': u'E', u'е': u'e',
    u'Ж': u'Ž', u'ж': u'ž',
    u'З': u'Z', u'з': u'z',
    u'И': u'I', u'и': u'i',
    u'Ј': u'J', u'ј': u'j',
    u'К': u'K', u'к': u'k',
    u'Л': u'L', u'л': u'l',
    u'Љ': u'Lj', u'љ': u'lj',
    u'М': u'M', u'м': u'm',
    u'Н': u'N', u'н': u'n',
    u'Њ': u'Nj', u'њ': u'nj',
    u'О': u'O', u'о': u'o',
    u'П': u'P', u'п': u'p',
    u'Р': u'R', u'р': u'r',
    u'С': u'S', u'с': u's',
    u'Т': u'T', u'т': u't',
    u'Ћ': u'Ć', u'ћ': u'ć',
    u'У': u'U', u'у': u'u',
    u'Ф': u'F', u'ф': u'f',
    u'Х': u'H', u'х': u'h',
    u'Ц': u'C', u'ц': u'c',
    u'Ч': u'Č', u'ч': u'č',
    u'Џ': u'Dž', u'џ': u'dž',
    u'Ш': u'Š', u'ш': u'š',
}

# This dictionary is to transliterate from Serbian latin to cyrillic.
# Let's build it by simply swapping keys and values of previous dictionary.
SR_LAT_TO_CYR_DICT = {y: x for x, y in iter(SR_CYR_TO_LAT_DICT.items())}

# Build the dictionaries to transliterate Montenegrin cyrillic to latin and vice versa.

# Montenegrin Latin is based on Serbo-Croatian Latin, with the addition of the two letters Ś and Ź,
# to replace the digraphs SJ and ZJ.
# These parallel the two letters of the Montenegrin Cyrillic alphabet not found in Serbian, С́ and З́.
# These, respectively, could also be represented in the original alphabets as šj and žj, and шj and жj.
# Source: https://en.wikipedia.org/wiki/Montenegrin_alphabet#Latin_alphabet
# Also see: http://news.bbc.co.uk/2/hi/8520466.stm
ME_CYR_TO_LAT_DICT = copy.deepcopy(SR_CYR_TO_LAT_DICT)
ME_CYR_TO_LAT_DICT.update({
    u'С́': u'Ś', u'с́': u'ś',  # Montenegrin
    u'З́': u'Ź', u'з́': u'ź'  # Montenegrin
})

# This dictionary is to transliterate from Montenegrin latin to cyrillic.
ME_LAT_TO_CYR_DICT = {y: x for x, y in iter(ME_CYR_TO_LAT_DICT.items())}

# Build the dictionaries to transliterate Macedonian cyrillic to latin and vice versa.
MK_CYR_TO_LAT_DICT = copy.deepcopy(SR_CYR_TO_LAT_DICT)

# Differences with Serbian:
# 1) Between Ze (З з) and I (И и) is the letter Dze (Ѕ ѕ), which looks like the Latin letter S and represents /d͡z/.
MK_CYR_TO_LAT_DICT[u'Ѕ'] = u'Dz'
MK_CYR_TO_LAT_DICT[u'ѕ'] = u'dz'

# 2) Dje (Ђ ђ) is replaced by Gje (Ѓ ѓ), which represents /ɟ/ (voiced palatal stop).
# In some dialects, it represents /d͡ʑ/ instead, like Dje
# It is written ⟨Ǵ ǵ⟩ in the corresponding Macedonian Latin alphabet.
del MK_CYR_TO_LAT_DICT[u'Ђ']
del MK_CYR_TO_LAT_DICT[u'ђ']
MK_CYR_TO_LAT_DICT[u'Ѓ'] = u'Ǵ'
MK_CYR_TO_LAT_DICT[u'ѓ'] = u'ǵ'

# 3) Tshe (Ћ ћ) is replaced by Kje (Ќ ќ), which represents /c/ (voiceless palatal stop).
# In some dialects, it represents /t͡ɕ/ instead, like Tshe.
# It is written ⟨Ḱ ḱ⟩ in the corresponding Macedonian Latin alphabet.
del MK_CYR_TO_LAT_DICT[u'Ћ']
del MK_CYR_TO_LAT_DICT[u'ћ']
MK_CYR_TO_LAT_DICT[u'Ќ'] = u'Ḱ'
MK_CYR_TO_LAT_DICT[u'ќ'] = u'ḱ'

# This dictionary is to transliterate from Macedonian latin to cyrillic.
MK_LAT_TO_CYR_DICT = {y: x for x, y in iter(MK_CYR_TO_LAT_DICT.items())}

# This dictionary is to transliterate from cyrillic to latin.
RU_CYR_TO_LAT_DICT = {
    u"А": u"A", u"а": u"a",
    u"Б": u"B", u"б": u"b",
    u"В": u"V", u"в": u"v",
    u"Г": u"G", u"г": u"g",
    u"Д": u"D", u"д": u"d",
    u"Е": u"E", u"е": u"e",
    u"Ё": u"YO", u"ё": u"yo",
    u"Ж": u"ZH", u"ж": u"zh",
    u"З": u"Z", u"з": u"z",
    u"И": u"I", u"и": u"i",
    u"Й": u"J", u"й": u"j",
    u"К": u"K", u"к": u"k",
    u"Л": u"L", u"л": u"l",
    u"М": u"M", u"м": u"m",
    u"Н": u"N", u"н": u"n",
    u"О": u"O", u"о": u"o",
    u"П": u"P", u"п": u"p",
    u"Р": u"R", u"р": u"r",
    u"С": u"S", u"с": u"s",
    u"Т": u"T", u"т": u"t",
    u"У": u"U", u"у": u"u",
    u"Ф": u"F", u"ф": u"f",
    u"Х": u"H", u"х": u"h",
    u"Ц": u"C", u"ц": u"c",
    u"Ч": u"CH", u"ч": u"ch",
    u"Ш": u"SH", u"ш": u"sh",
    u"Щ": u"SZ", u"щ": u"sz",
    u"Ъ": u"#", u"ъ": u"#",
    u"Ы": u"Y", u"ы": u"y",
    u"Ь": u"", u"ь": u"",
    u"Э": u"E", u"э": u"e",
    u"Ю": u"JU", u"ю": u"ju",
    u"Я": u"JA", u"я": u"ja",
}

# This dictionary is to transliterate from Russian latin to cyrillic.
RU_LAT_TO_CYR_DICT = {y: x for x, y in iter(RU_CYR_TO_LAT_DICT.items())}
RU_LAT_TO_CYR_DICT.update({
    u"X": u"Х", u"x": u"х",
    u"W": u"Щ", u"w": u"щ",
    u"'": u"ь",
    u"#": u"ъ",
    u"JE": u"ЖЕ", u"Je": u"Же", u"je": u"же",
    u"YU": u"Ю", u"Yu": u"Ю", u"yu": u"ю",
    u"YA": u"Я", u"Ya": u"Я", u"ya": u"я",
    u"iy": u"ый",  # dobriy => добрый
})

# Transliterate from Tajik cyrillic to latin
TJ_CYR_TO_LAT_DICT = copy.deepcopy(RU_CYR_TO_LAT_DICT)
# Change Mapping according to ISO 9 (1995)
TJ_CYR_TO_LAT_DICT[u"Э"] = u"È"
TJ_CYR_TO_LAT_DICT[u"э"] = u"è"
TJ_CYR_TO_LAT_DICT[u"ъ"] = u"’"
TJ_CYR_TO_LAT_DICT[u"Ч"] = u"Č"
TJ_CYR_TO_LAT_DICT[u"ч"] = u"č"
TJ_CYR_TO_LAT_DICT[u"Ж"] = u"Ž"
TJ_CYR_TO_LAT_DICT[u"ж"] = u"ž"
TJ_CYR_TO_LAT_DICT[u"Ё"] = u"Ë"
TJ_CYR_TO_LAT_DICT[u"ё"] = u"ë"
TJ_CYR_TO_LAT_DICT[u"Ш"] = u"Š"
TJ_CYR_TO_LAT_DICT[u"ш"] = u"š"
TJ_CYR_TO_LAT_DICT[u"Ю"] = u"Û"
TJ_CYR_TO_LAT_DICT[u"ю"] = u"û"
TJ_CYR_TO_LAT_DICT[u"Я"] = u"Â"
TJ_CYR_TO_LAT_DICT[u"я"] = u"â"
# delete letters not used
del TJ_CYR_TO_LAT_DICT[u"Ц"]
del TJ_CYR_TO_LAT_DICT[u"ц"]
del TJ_CYR_TO_LAT_DICT[u"Щ"]
del TJ_CYR_TO_LAT_DICT[u"щ"]
del TJ_CYR_TO_LAT_DICT[u"Ы"]
del TJ_CYR_TO_LAT_DICT[u"ы"]

# update the dict for the additional letters in the tajik cyrillic alphabet ( Ғ, Ӣ, Қ, Ӯ, Ҳ, Ҷ )
# see https://en.wikipedia.org/wiki/Tajik_alphabet#Cyrillic
TJ_CYR_TO_LAT_DICT.update({
    u"Ғ": u"Ǧ", u"ғ": u"ǧ",
    u"Ӣ": u"Ī", u"ӣ": u"ī",
    u"Қ": u"Q", u"қ": u"q",
    u"Ӯ": u"Ū", u"ӯ": u"ū",
    u"Ҳ": u"Ḩ", u"ҳ": u"ḩ",
    u"Ҷ": u"Ç", u"ҷ": u"ç"
})

# transliterate from latin tajik to cyrillic
TJ_LAT_TO_CYR_DICT = {y: x for x, y in iter(TJ_CYR_TO_LAT_DICT.items())}

# Bundle up all the dictionaries in a lookup dictionary
TRANSLIT_DICT = {
    'sr': {  # Serbia
        'tolatin': SR_CYR_TO_LAT_DICT,
        'tocyrillic': SR_LAT_TO_CYR_DICT
    },
    'me': {  # Montenegro
        'tolatin': ME_CYR_TO_LAT_DICT,
        'tocyrillic': ME_LAT_TO_CYR_DICT
    },
    'mk': {  # Macedonia
        'tolatin': MK_CYR_TO_LAT_DICT,
        'tocyrillic': MK_LAT_TO_CYR_DICT
    },
    'ru': {  # Russian
        'tolatin': RU_CYR_TO_LAT_DICT,
        'tocyrillic': RU_LAT_TO_CYR_DICT
    },
    'tj': {  # Tajik
        'tolatin': TJ_CYR_TO_LAT_DICT,
        'tocyrillic': TJ_LAT_TO_CYR_DICT
    },
}


def __encode_utf8(_string):
    if sys.version_info < (3, 0):
        return _string.encode('utf-8')
    else:
        return _string


def __decode_utf8(_string):
    if sys.version_info < (3, 0):
        return _string.decode('utf-8')
    else:
        return _string


def to_latin(string_to_transliterate, lang_code='sr'):
    ''' Transliterate serbian cyrillic string of characters to latin string of characters.
    :param string_to_transliterate: The cyrillic string to transliterate into latin characters.
    :param lang_code: Indicates the cyrillic language code we are translating from. Defaults to Serbian (sr).
    :return: A string of latin characters transliterated from the given cyrillic string.
    '''

    # First check if we support the cyrillic alphabet we want to transliterate to latin.
    if lang_code.lower() not in TRANSLIT_DICT:
        # If we don't support it, then just return the original string.
        return string_to_transliterate

    # If we do support it, check if the implementation is not missing before proceeding.
    elif not TRANSLIT_DICT[lang_code.lower()]['tolatin']:
        return string_to_transliterate

    # Everything checks out, proceed with transliteration.
    else:

        # Get the character per character transliteration dictionary
        transliteration_dict = TRANSLIT_DICT[lang_code.lower()]['tolatin']

        # Initialize the output latin string variable
        latinized_str = ''

        # Transliterate by traversing the input string character by character.
        string_to_transliterate = __decode_utf8(string_to_transliterate)

        for c in string_to_transliterate:

            # If character is in dictionary, it means it's a cyrillic so let's transliterate that character.
            if c in transliteration_dict:
                # Transliterate current character.
                latinized_str += transliteration_dict[c]

            # If character is not in character transliteration dictionary,
            # it is most likely a number or a special character so just keep it.
            else:
                latinized_str += c

        # Return the transliterated string.
        return __encode_utf8(latinized_str)


def to_cyrillic(string_to_transliterate, lang_code='sr'):
    ''' Transliterate serbian latin string of characters to cyrillic string of characters.
    :param string_to_transliterate: The latin string to transliterate into cyrillic characters.
    :param lang_code: Indicates the cyrillic language code we are translating to. Defaults to Serbian (sr).
    :return: A string of cyrillic characters transliterated from the given latin string.
    '''

    # First check if we support the cyrillic alphabet we want to transliterate to latin.
    if lang_code.lower() not in TRANSLIT_DICT:
        # If we don't support it, then just return the original string.
        return string_to_transliterate

    # If we do support it, check if the implementation is not missing before proceeding.
    elif not TRANSLIT_DICT[lang_code.lower()]['tocyrillic']:
        return string_to_transliterate

    else:
        # Get the character per character transliteration dictionary
        transliteration_dict = TRANSLIT_DICT[lang_code.lower()]['tocyrillic']

        # Initialize the output cyrillic string variable
        cyrillic_str = ''

        string_to_transliterate = __decode_utf8(string_to_transliterate)

        # Transliterate by traversing the inputted string character by character.
        length_of_string_to_transliterate = len(string_to_transliterate)
        index = 0

        while index < length_of_string_to_transliterate:
            # Grab a character from the string at the current index
            c = string_to_transliterate[index]

            # Watch out for Lj and lj. Don't want to interpret Lj/lj as L/l and j.
            # Watch out for Nj and nj. Don't want to interpret Nj/nj as N/n and j.
            # Watch out for Dž and and dž. Don't want to interpret Dž/dž as D/d and j.
            c_plus_1 = u''
            if index != length_of_string_to_transliterate - 1:
                c_plus_1 = string_to_transliterate[index + 1]

            if ((c == u'L' or c == u'l') and c_plus_1 == u'j') or \
                    ((c == u'N' or c == u'n') and c_plus_1 == u'j') or \
                    ((c == u'D' or c == u'd') and c_plus_1 == u'ž') or \
                    (lang_code == 'mk' and (c == u'D' or c == u'd') and c_plus_1 == u'z') or \
                    (lang_code == 'ru' and (
                            (c in u'Cc' and c_plus_1 in u'Hh') or  # c, ch
                            (c in u'Ee' and c_plus_1 in u'Hh') or  # eh
                            (c == u'i' and c_plus_1 == u'y' and
                             string_to_transliterate[index + 2:index + 3] not in u'aou') or  # iy[^AaOoUu]
                            (c in u'Jj' and c_plus_1 in u'UuAaEe') or  # j, ju, ja, je
                            (c in u'Ss' and c_plus_1 in u'HhZz') or  # s, sh, sz
                            (c in u'Yy' and c_plus_1 in u'AaOoUu') or  # y, ya, yo, yu
                            (c in u'Zz' and c_plus_1 in u'Hh')  # z, zh
                    )):
                index += 1
                c += c_plus_1

            # If character is in dictionary, it means it's a cyrillic so let's transliterate that character.
            if c in transliteration_dict:
                # ay, ey, iy, oy, uy
                if lang_code == 'ru' and c in u'Yy' and \
                        cyrillic_str and cyrillic_str[-1].lower() in u"аеиоуэя":
                    cyrillic_str += u"й" if c == u'y' else u"Й"
                else:
                    # Transliterate current character.
                    cyrillic_str += transliteration_dict[c]

            # If character is not in character transliteration dictionary,
            # it is most likely a number or a special character so just keep it.
            else:
                cyrillic_str += c

            index += 1

        return __encode_utf8(cyrillic_str)


def supported():
    ''' Returns list of supported languages
    :return:
    '''
    return TRANSLIT_DICT.keys()
