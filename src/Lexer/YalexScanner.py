from copy import copy as cp


class RegularDef:
    def __init__(self, name: str, definition: str) -> None:
        self.name: str = name
        self.regex: str = definition

    def __repr__(self) -> str:
        return f'{self.name} : {self.definition}'


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
                info = line[3:]
                new_def = self._getDefinition(info)
                self.regexDefs.append(new_def)
                self._process_regex(new_def)

    def _process_regex(self, definition: RegularDef) -> None:
        regex = list(cp(definition.regex))

        if regex[0] == '[':
            if regex[-1] != ']':
                def_string = definition.__repr__()
                print(f'Error Lexico: Expresion invalida "{def_string}"')
                return

            definition.regex = self._raw_exp(regex[1:-1])
            return

    def _getDefinition(self, line: list) -> RegularDef:
        line = list(line)
        new_name = ''
        new_def = ''
        name_readed = False

        while len(line) > 0:
            actual = line.pop(0)
            lookAhead = line[0] if len(line) > 0 else ''

            if actual == ' ' and lookAhead == '=':
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

        return regex

    def __repr__(self) -> str:
        string = ''

        for regex in self.regexDefs:
            string += regex.__repr__()

        return string
