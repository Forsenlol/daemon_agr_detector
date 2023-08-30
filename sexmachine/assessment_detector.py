import os.path


class AssessmentDetector:
    def __init__(self, file_name):

        """Creates a detector parsing given data file"""
        self._parse(os.path.join(os.path.dirname(__file__), "data/" + file_name))

    def _parse(self, file):
        """Opens data file and for each line, calls _eat_name_line"""
        self.names = {}
        with open(file, 'r') as infile:
            for row in infile:
                gender, username = row.strip().split(',')
                if gender == '1':
                    self._set(username, 'male', 1)
                if gender == '2':
                    self._set(username, 'female', 1)
                if gender == '3':
                    self._set(username, 'brand', 1)

    def add(self, username, gender):
        self._set(username, gender, 1)

    def _set(self, name, gender, country_values):
        if name not in self.names:
            self.names[name] = {}
        self.names[name][gender] = country_values

    def _most_popular_gender(self, name, counter):
        """Finds the most popular gender for the given name counting by given counter"""
        if name not in self.names:
            return u"unknown"

        max_count, max_tie = (0, 0)
        best = list(self.names[name].keys())[0]
        for gender, country_values in list(self.names[name].items()):
            count, tie = counter(country_values)
            if count > max_count or (count == max_count and tie > max_tie):
                max_count, max_tie, best = count, tie, gender

        return best if max_count > 0 else u"andy"

    def get_gender(self, name):
        name = str(name).lower()

        if name not in self.names:
            return u"unknown"

        # elif not country:
        def counter(country_values):
            return country_values, 0

        return self._most_popular_gender(name, counter)
