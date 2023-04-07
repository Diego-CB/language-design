from copy import copy as cp

RESERVED = ['|', '*', '?', '+', '(', ')']


class RegularDef:
    def __init__(self, name: list, definition: list) -> None:
        self.name: list = name
        self.regex: list = definition

    def __repr__(self) -> str:
        return f'{self.name} = {self.regex}'


class Token:
    def __init__(self) -> None:
        self.rule: list = ''
        self.token: list = ''

    def __repr__(self) -> str:
        return f'{self.token} = {self.rule}'


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
        self.tokenRules: list = []
        self.alphabet: list[str] = []
        rulesLines = []
        rulesFlag = False

        for line in lines:
            prefix = line.split(' ')[0]

            match prefix:
                # Manejo de definiciones regulares
                case 'let':
                    info = line[3:-1]
                    new_def = self._getDefinition(info)
                    self.ogDefs.append(new_def.__repr__())
                    new_def.regex = self._process_regex(new_def.regex)
                    self.regexDefs.append(new_def)

                # guardar lineas de definicion de rules
                case 'rule':
                    rulesFlag = True

                case '(*':
                    pass

                case _:
                    if not rulesFlag:
                        continue

                    if (
                        (
                            len(rulesLines) == 0
                            or self._firstCHarInLine(line) == '|'
                        ) and len(line) > 1
                    ):
                        rulesLines.append(list(line))

        self._process_ruleTokens(rulesLines)
        self.unifiedRegex = self._getFinalRegex()
        self.printFile()

    def _getFinalRegex(self) -> str:
        expresions = []

        for token in self.tokenRules:
            expresions.append(token.rule)

        return self._toRegexOr(expresions)

    def _process_ruleTokens(self, rulesLines) -> None:
        for exp in rulesLines:
            rule: Token = Token()
            reading_def = True
            token_readed = False

            while len(exp) > 0 and not token_readed:
                actual = exp.pop(0)

                if actual == '|':
                    continue

                if actual == ' ' and reading_def:
                    continue

                if actual == '{':
                    reading_def = False
                    rule.rule = self._process_regex(rule.rule)
                    continue

                if not reading_def:
                    if actual == '}':
                        token_readed = True
                        rule.token = self._process_token(rule.token)
                        self.tokenRules.append(rule)
                        continue

                    rule.token += actual

                else:
                    rule.rule += actual

    def _process_token(self, token: list) -> str:
        token = token[1:] if token[0] == ' ' else token
        token = token[:-1] if token[-1] == ' ' else token
        return_stm, token_name = token.split(' ')
        return token_name

    def _firstCHarInLine(self, line):
        line = list(line)
        actual = line.pop(0)

        while actual == ' ':
            actual = line.pop(0)

        return actual

    def _getDefinition(self, line: list) -> RegularDef:
        line = list(line)
        new_name = []
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
                new_name.append(ord(actual))

        return RegularDef(new_name, new_def)

    def _process_regex(self, definition: str) -> None:
        regex = list(definition)

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

            return self._raw_exp(regex[1:-1])

        # Manejo de definiciones que referencian definiciones previas
        regex = regex[:-1] if regex[-1] == '\n' else list(regex)
        return self._recursive_expresion(regex)

    def _recursive_expresion(self, regex: list) -> str:
        og_regex = cp(regex)
        definitions = self.regexDefs
        regex_names = [regex.name for regex in definitions]
        # TODO no se puede usar una lista como key de ditionary
        starters = [regex[0] for regex in regex_names]
        out_regex = []

        while len(regex) > 0:
            actual = ord(regex.pop(0))

            # Referencias a definiciones pasadas
            if actual in starters:
                posible_defs = []

                for index, char in enumerate(starters):
                    if actual == char:
                        posible_defs.append(regex_names[index])

                char_count = 1
                founded_def = None
                backTrace = [actual]

                while len(posible_defs) > 0:
                    actual = ord(regex.pop(0))
                    lookAhead = ord(regex[0]) if len(regex) > 0 else None
                    not_defs = []

                    for def_ in posible_defs:
                        if actual != def_[char_count]:
                            not_defs.append(def_)

                        if len(def_) > char_count + 1 and lookAhead != def_[char_count + 1]:
                            not_defs.append(def_)

                        if actual == def_[char_count] and len(def_) == char_count + 1:
                            founded_def = def_
                            not_defs.append(def_)

                    for def_ in not_defs:
                        if def_ in posible_defs:
                            posible_defs.remove(def_)

                    char_count += 1
                    backTrace.append(actual)

                if founded_def is not None:
                    def_index = regex_names.index(founded_def)
                    founded_regex = definitions[def_index].regex
                    out_regex = out_regex + founded_regex

                else:
                    out_regex = out_regex + backTrace

                continue

            # Caracteres Nuevos
            if actual in [ord("'"), ord('"')]:
                raw_exp = [chr(actual)]
                actual = ''

                while actual not in ["'", '"']:
                    actual = regex.pop(0)
                    raw_exp.append(actual)

                out_regex = out_regex + self._raw_exp(raw_exp)
                continue

            # Secuencias de Caracteres Nuevos
            if actual == ord('['):
                raw_exp = []

                while actual != ']':
                    if len(regex) < 0:
                        print(f'(Error Lexico) Expresion invalida: {og_regex}')
                        return og_regex

                    actual = regex.pop(0)

                    if actual != ']':
                        raw_exp.append(actual)

                out_regex = out_regex + self._raw_exp(raw_exp)
                continue

            if (
                chr(actual) not in RESERVED
                and actual not in self.alphabet
            ):
                self.alphabet.append(actual)

            if chr(actual) not in RESERVED:
                out_regex.append(actual)

            else:
                out_regex.append(chr(actual))

        return out_regex

    def _raw_exp(self, regex: list) -> str:
        expresions: list = []
        reading_exp: bool = False
        secuence_start = None
        secuence_end = None

        while len(regex) > 0:
            actual = ord(regex.pop(0))
            lookAhead = ord(regex[0]) if len(regex) > 0 else None

            if actual in [ord("'"), ord('"')]:
                reading_exp = not reading_exp
                if not reading_exp and secuence_start is not None:
                    secuence_end = expresions[-1]

            if reading_exp:
                if actual in [ord("'"), ord('"')]:
                    continue

                new_exp = actual

                if actual == ord('\\'):
                    if lookAhead == ord('n'):
                        new_exp = ord('\n')
                    elif lookAhead == ord('t'):
                        new_exp = ord('\t')
                    elif lookAhead == ord('s'):
                        new_exp = ord(' ')
                    regex.pop(0)

                expresions.append(new_exp)

                if new_exp not in self.alphabet:
                    self.alphabet.append(new_exp)

            if actual == ord('-') and not reading_exp:
                secuence_start = expresions[-1]

            if secuence_start is not None and secuence_end is not None:
                start = secuence_start + 1
                end = secuence_end

                while start < end:
                    if start not in self.alphabet:
                        self.alphabet.append(start)
                    expresions.append(start)
                    start += 1

                secuence_end = None
                secuence_start = None

        if secuence_start is not None or reading_exp:
            regex = '[' + ''.join(regex) + ']'
            print('(Error Lexico) Expresion invalida:', regex)
            return regex

        return self._toRegexOr(expresions)

    def _toRegexOr(self, expresions: list) -> int | list:
        if len(expresions) == 1:
            return expresions

        or_exp: list = ['(']

        for exp in expresions:
            if len(or_exp) == 1:
                if type(exp) == list:
                    or_exp = or_exp + exp
                else:
                    or_exp.append(exp)
                continue

            or_exp.append('|')

            if type(exp) == list:
                or_exp = or_exp + exp

            else:
                or_exp.append(exp)

        or_exp.append(')')
        return or_exp

    def __repr__(self) -> str:
        string = '---- Original Definitions ----\n'
        return string

        for regex in self.ogDefs:
            string += '  -> '
            string += regex
            string += '\n'

        string += '\n---- Processed Definitions ----\n'

        for regex in self.regexDefs:
            string += '  -> '
            string += regex.__repr__()
            string += '\n'

        string += '\n---- Rules ----\n'

        for token in self.tokenRules:
            string += '  -> '
            string += token.__repr__()
            string += '\n'

        string += '\n---- Final Regex ----\n'
        string += self.unifiedRegex
        string += '\n'

        return string

    def printFile(self):
        f = open('./out/steps.txt', 'w')
        f.write(self.__repr__())
        f.close()
