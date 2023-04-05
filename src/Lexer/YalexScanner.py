import sys


class RegularDef:
    def __init__(self, name: str, definition: str) -> None:
        self.name: str = name
        self.definition: str = self._process_regex(definition)

    def _process_regex(regex: str) -> str:
        return regex

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

    def _getDefinition(self, line: list) -> RegularDef:
        line = list(line)
        new_name = ''
        new_def = ''
        name_readed = False

        while len(line) > 0:
            actual = line.pop(0)
            lookAhead = line[0] if len(line) > 0 else ''

            if actual == ' ' and lookAhead == '=':
                line.pop(0)
                if line[0] == ' ':
                    line.pop(0)

                name_readed = True
                continue

            if name_readed:
                new_def += actual

            else:
                new_name += actual

        return RegularDef(new_name, new_def)

    def __repr__(self) -> str:
        string = ''

        for regex in self.regexDefs:
            string += regex.__repr__()

        return string


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input Yalex File Missing')

    # Read Input File
    filepath = sys.argv[1]
    reader: YalexReader = YalexReader(filename=filepath)
    print(reader)
