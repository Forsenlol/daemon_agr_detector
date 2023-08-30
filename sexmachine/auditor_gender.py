import os
import re
import unicodedata
from typing import Optional

import sexmachine.detector as gender
from sexmachine.assessment_detector import AssessmentDetector
from sexmachine.usa_baby_detector import UsaBabyDetector
from sexmachine.utils import to_latin

gender_detector, usa_baby_detector = None, None
ha_name_detector = UsaBabyDetector(path="data/names/hypeauditor_rules.txt")
assessment_detector = AssessmentDetector('platform_assessment.csv')
ha_assessment_detector = AssessmentDetector('auditor_assessment.csv')


def most_common(lst):
    return max(set(lst), key=lst.count)


def get_detectors():
    global gender_detector, usa_baby_detector

    if gender_detector is not None:
        return gender_detector, usa_baby_detector

    gender_detector = gender.Detector(case_sensitive=False)
    usa_baby_detector = UsaBabyDetector()

    return gender_detector, usa_baby_detector


countries = []
with open(os.path.join(os.path.dirname(__file__), "data/countries.txt"), 'r') as file:
    for row in file:
        name = row.strip().lower()
        countries.append(name)


def add_to_ha_assessment(username, gender):
    with open(os.path.join(os.path.dirname(__file__), "data/auditor_assessment.csv"), 'a') as file:
        if gender == 'male':
            file.write('1,' + username + '\n')
        elif gender == 'female':
            file.write('2,' + username + '\n')
        elif gender == 'brand':
            file.write('3,' + username + '\n')
        ha_assessment_detector.add(username, gender)


def get_gender_single_word(word):
    test = ha_name_detector.get_gender(word)
    if test != 'unknown':
        return test, 'ha_name'

    _gender_detector, _usa_baby_detector = get_detectors()

    test = _gender_detector.get_gender(word)
    if test != 'unknown':
        return test, 'sexmachine'

    if _usa_baby_detector is not None:
        test = _usa_baby_detector.get_gender(word)
        if test != 'unknown':
            return test, 'usa'

    return 'unknown', None


def get_auditor_gender(username, full_name, *, assessment: Optional[dict] = None) -> (str, str):
    """Проверяем сначала в ассесменте"""
    if assessment:
        demography_aggregation_data = assessment.get('assessment', {})
        blogger_gender = demography_aggregation_data.get('brender')
        if blogger_gender in ['male', 'female']:
            return blogger_gender, 'assessment'

    assessment_result = ha_assessment_detector.get_gender(username)
    if assessment_result != 'unknown':
        return assessment_result, 'ha_assessment'

    assessment_result = assessment_detector.get_gender(username)
    if assessment_result != 'unknown':
        return assessment_result, 'assessment'

    decoded_name = to_latin(full_name, lang_code='ru')
    decoded_name = unicodedata.normalize('NFKD', decoded_name).encode('ASCII', 'ignore').decode("utf-8")
    words = []
    for x in split_words(decoded_name):
        test_name = x.lower()
        #  Пропускаем страну
        if test_name in countries:
            continue
        # Важен порядок в котором добавляем, поэтому не list(set)
        if test_name not in words:
            words.append(test_name)
    if len(words) == 0 or len(words) > 3:
        if username != '':
            if '.' in username or '_' in username:
                return get_auditor_gender('', username.replace('_', ' ').replace('.', ' '))
        return 'unknown', 'n/a'

    results = []
    source_list = []
    for word in words:
        processed_word = word
        gender_test, source = get_gender_single_word(processed_word)

        if gender_test != 'unknown':
            results.append(gender_test)
            source_list.append(processed_word + '=' + source + '(' + gender_test + ')')
    if len(results) == 0:
        return 'unknown', 'n/a'

    if 'male' in results or 'female' in results:
        results = list(filter(lambda x: x not in ['mostly_male', 'mostly_female', 'andy'], results))
    elif 'mostly_male' in results or 'mostly_female' in results:
        results = list(filter(lambda x: x not in ['andy'], results))
    else:
        return 'unknown', 'n/a'

    if len(results) <= 2:
        return results[0], ','.join(source_list)

    return most_common(results), ','.join(source_list)


def split_words(full_name: str):
    full_name = full_name.replace('_', ' ')
    rgx = re.compile("([\w][\w']*\w)")
    temp = rgx.findall(full_name)
    return temp
