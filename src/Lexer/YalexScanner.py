from copy import copy as cp


class RegularDef:
    def __init__(self, name: str, definition: str) -> None:
        self.name: str = name
        self.regex: str = definition

    def __repr__(self) -> str:
        return f'{self.name} -> {self.regex}'


class YalexReader:
    def __init__(self, filename: str) -> None:

        # File Reading
        file = open(filename)
        lines = file.readlines()
        file.close()

        # Get Regular Definitions from input File
        self.regexDefs: list[RegularDef] = []

        for line in lines:
            if line.split(' ')[0] == 'let':
                info = line[3:-1]
                new_def = self._getDefinition(info)
                self.regexDefs.append(new_def)
                self._process_regex(new_def)

    def _process_regex(self, definition: RegularDef) -> None:
        regex = list(definition.regex)

        if regex[0] == '[':
            index = len(regex) - 1
            actual = None

            while actual != ']':
                actual = regex[index]

                if actual != ']':
                    regex.pop(index)

                index -= 1

                if index < 0:
                    def_string = definition.__repr__()
                    print(f'(Error Lexico) Expresion invalida: {def_string}')
                    return

            definition.regex = self._raw_exp(regex[1:-1])
            return

        return

    def _getDefinition(self, line: list) -> RegularDef:
        line = list(line)
        new_name = ''
        new_def = ''
        name_readed = False

        while len(line) > 0:
            actual = line.pop(0)
            lookAhead = line[0] if len(line) > 0 else ''

            if actual == ' ':
                if lookAhead == '=':
                    name_readed = True
                    line.pop(0)

                    if line[0] == ' ':
                        line.pop(0)

                continue

            if name_readed:
                new_def += actual

            else:
                new_name += actual

        return RegularDef(new_name, new_def)

    def _raw_exp(self, regex: str) -> str:
        expresions: list = []
        reading_exp: bool = False
        secuence_start = None
        secuence_end = None

        while len(regex) > 0:
            actual = regex.pop(0)
            lookAhead = regex[0] if len(regex) > 0 else None

            if actual == "'":
                reading_exp = not reading_exp
                if not reading_exp and secuence_start is not None:
                    secuence_end = expresions[-1]

            if reading_exp:
                if actual == "'":
                    continue

                new_exp = actual

                if actual == '\\':
                    if lookAhead == 'n':
                        new_exp = '\n'
                    elif lookAhead == 't':
                        new_exp = '\t'
                    regex.pop(0)

                expresions.append(new_exp)

            if actual == '-':
                secuence_start = expresions[-1]
                secuence_end = None

            if secuence_start is not None and secuence_end is not None:
                start = ord(secuence_start) + 1
                end = ord(secuence_end)

                while start < end:
                    string_char = chr(start)
                    expresions.append(string_char)
                    start += 1

                secuence_end = None
                secuence_start = None

        return self._toRegexOr(expresions)

    def _toRegexOr(self, expresions: list) -> str:
        or_exp: list = []

        for exp in expresions:
            if len(or_exp) == 0:
                or_exp.append(exp)
                continue

            or_exp.insert(0, '(')
            or_exp.append('|')
            or_exp.append(exp)
            or_exp.append(')')

        return ''.join(or_exp)

    def __repr__(self) -> str:
        string = ''

        for regex in self.regexDefs:
            string += regex.__repr__()
            string += '\n'

        return string
