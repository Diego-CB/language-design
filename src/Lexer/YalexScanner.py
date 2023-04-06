from copy import copy as cp


class RegularDef:
    def __init__(self, name: str, definition: str) -> None:
        self.name: str = name
        self.regex: str = definition

    def __repr__(self) -> str:
        return f'{self.name} = {self.regex}'


class YalexReader:
    # TODO: Comments on YalexReader file
    def __init__(self, filename: str) -> None:
        # File Reading
        file = open(filename)
        lines = file.readlines()
        file.close()

        # Get Regular Definitions from input File
        self.regexDefs: list[RegularDef] = []
        self.ogDefs: list[str] = []

        for line in lines:
            if line.split(' ')[0] == 'let':
                info = line[3:-1]
                new_def = self._getDefinition(info)
                self.ogDefs.append(new_def.__repr__())
                self._process_regex(new_def)
                self.regexDefs.append(new_def)

            # TODO: Rules processing

    def _getDefinition(self, line: list) -> RegularDef:
        line = list(line)
        new_name = ''
        new_def = ''
        name_readed = False

        while line[0] == ' ':
            line.pop(0)

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

    def _process_regex(self, definition: RegularDef) -> None:
        regex = list(definition.regex)

        # Manejo de definiciones nuevas
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

        # Manejo de definiciones que referencian definiciones previas
        regex = regex[:-1] if regex[-1] == '\n' else list(regex)
        definition.regex = self._recursive_expresion(regex)

    def _recursive_expresion(self, regex: list) -> str:
        # return ''.join(regex)
        og_regex = cp(regex)
        definitions = self.regexDefs
        regex_names = [regex.name for regex in definitions]
        def_map = {regex.name: regex.regex for regex in definitions}
        starters = [regex[0] for regex in regex_names]
        out_regex = ''

        while len(regex) > 0:
            actual = regex.pop(0)

            # Referencias a definiciones pasadas
            if actual in starters:
                posible_defs = []

                for index, char in enumerate(starters):
                    if actual == char:
                        posible_defs.append(regex_names[index])

                char_count = 1
                founded_def = None
                backTrace = actual

                while len(posible_defs) > 0:
                    actual = regex.pop(0)
                    not_defs = []

                    for def_ in posible_defs:
                        if actual != def_[char_count]:
                            not_defs.append(def_)

                        if actual == def_[char_count] and len(def_) == char_count + 1:
                            founded_def = def_
                            not_defs.append(def_)

                    for def_ in not_defs:
                        posible_defs.remove(def_)

                    char_count += 1
                    backTrace += actual

                if founded_def is not None:
                    out_regex += def_map[founded_def]
                else:
                    out_regex += backTrace

                continue

            # Caracteres Nuevos
            if actual in ['"', "'"]:
                raw_exp = [actual]
                actual = ''

                while actual not in ['"', "'"]:
                    actual = regex.pop(0)
                    raw_exp.append(actual)

                out_regex += self._raw_exp(raw_exp)
                continue

            # Secuencias de Caracteres Nuevos
            if actual == '[':
                raw_exp = []

                while actual != ']':
                    if len(regex) < 0:
                        print(f'(Error Lexico) Expresion invalida: {og_regex}')
                        return og_regex

                    actual = regex.pop(0)

                    if actual != ']':
                        raw_exp.append(actual)

                out_regex += self._raw_exp(raw_exp)
                continue

            out_regex += actual

        return out_regex

    def _raw_exp(self, regex: list) -> str:
        expresions: list = []
        reading_exp: bool = False
        secuence_start = None
        secuence_end = None

        while len(regex) > 0:
            actual = regex.pop(0)
            lookAhead = regex[0] if len(regex) > 0 else None

            if actual in ["'", '"']:
                reading_exp = not reading_exp
                if not reading_exp and secuence_start is not None:
                    secuence_end = expresions[-1]

            if reading_exp:
                if actual in ["'", '"']:
                    continue

                new_exp = actual

                if actual == '\\':
                    if lookAhead == 'n':
                        new_exp = '\n'
                    elif lookAhead == 't':
                        new_exp = '\t'
                    regex.pop(0)

                expresions.append(new_exp)

            if actual == '-' and not reading_exp:
                secuence_start = expresions[-1]

            if secuence_start is not None and secuence_end is not None:
                start = ord(secuence_start) + 1
                end = ord(secuence_end)

                while start < end:
                    string_char = chr(start)
                    expresions.append(string_char)
                    start += 1

                secuence_end = None
                secuence_start = None

        if secuence_start is not None or reading_exp:
            regex = '[' + ''.join(regex) + ']'
            print('(Error Lexico) Expresion invalida:', regex)
            return regex

        return self._toRegexOr(expresions)

    def _toRegexOr(self, expresions: list) -> str:
        or_exp: str = ''

        for exp in expresions:
            if len(or_exp) == 0:
                or_exp = exp
                continue

            or_exp = '(' + or_exp
            or_exp += '|'
            or_exp += exp
            or_exp += ')'

        return or_exp

    def __repr__(self) -> str:
        string = '---- Original Definitions ----\n'

        for regex in self.ogDefs:
            string += '  - '
            string += regex
            string += '\n'

        string += '\n---- Processed Definitions ----\n'

        for regex in self.regexDefs:
            string += '  - '
            string += regex.__repr__()
            string += '\n'

        string += '\n---- Rules ----\n'

        string += '\n---- Final Regex ----\n'

        return string
