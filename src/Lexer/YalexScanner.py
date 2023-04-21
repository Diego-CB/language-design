'''
*************************************************
Universidad del Valle de Guatemala
Diseño de Lenguajes de Programación

YalexScanner.py
- Lector de archivos yalex.
  El output es una expresion regular
  que define un lenguaje.

Autor: Diego Cordova - 20212
*************************************************
'''

from copy import copy as cp
from .util import transformPostfix

RESERVED = ['|', '*', '?', '+', '(', ')']


class RegularDef:
    '''
    Objeto interno para representación de definiciones regulares

    Atributos:
        name (list): nombre de la definición regular
        regex (list): regex de la definición regular
    '''

    def __init__(self, name: list, definition: list) -> None:
        self.name: list = name
        self.regex: list = definition

    def __repr__(self) -> str:
        return f'{self.name} = {self.regex}'


class Token:
    '''
    Objeto interno para representación de reglas de tokens

    Atributos:
        name (rule): regex del token
        regex (code): Codigo asignado a este token
    '''

    def __init__(self) -> None:
        self.rule: list = ''
        self.code: list = ''

    def __repr__(self) -> str:
        return f'{self.rule} = {self.code}'


class YalexReader:
    '''
    Objeto Lector de Yalex

    Atributos:
        regexDefs (list[RegularDef]): definiciones regulares
        ogDefs (list[str]): Definiciones regulares isn procesar
        tokenRules (list[Token]): Reglas de tokens
        alphabet (list[str]): alphabeto del archivo yalex (lenguaje)
        unifiedRegex (list[str|int]): regex unificade que representa las reglas de tokens
    '''

    def _get_linePrefix(self, line: str) -> str:
        splited = line.split(' ')
        final_splited = []

        for split in splited:
            split = split.split('\t') if '\t' in split else [split]

            for section in split:
                if section != '':
                    final_splited.append(section)

        splited = final_splited
        prefix = splited.pop(0)
        line = ''

        for split in splited:
            line += split + ' '

        line = line[:-2] if line[-2:] == '\n ' else line
        return prefix, line

    def __init__(self, filename: str) -> None:
        # File Reading
        file = open(filename)
        lines = file.readlines()
        file.close()

        # Get Regular Definitions from input File
        self.regexDefs: list[RegularDef] = []
        self.ogDefs: list[str] = []
        self.tokenRules: list[Token] = []
        self.alphabet: list[str] = []
        rulesLines = []
        rulesFlag = False

        for line in lines:
            if rulesFlag:
                rulesLines.append(line)
                continue

            prefix, line = self._get_linePrefix(line)

            match prefix:
                # Manejo de definiciones regulares
                case 'let':
                    info = line
                    new_def = self._getDefinition(info)
                    self.ogDefs.append([new_def.name, new_def.regex])
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

        # Procesamiento de token rules
        self._process_ruleTokens(rulesLines)
        # Generacion de regex unificada
        self.unifiedRegex = self._getFinalRegex()
        self.printFile()

    def _getFinalRegex(self) -> str:
        ''' Genera regex unificada en base a self.tokenRules '''
        expresions = []

        for token in self.tokenRules:
            expresions.append(token.rule)

        return self._toRegexOr(expresions)

    def _process_ruleTokens(self, rulesLines) -> None:
        ''' Convierte los tokens a regex '''
        rules_stream = []

        for line in rulesLines:
            rules_stream = rules_stream + list(line)

        actual_rule: Token = Token()

        while len(rules_stream) > 0:
            actual = rules_stream.pop(0)

            if actual in ['|', ' ', '\n', '\t']:
                continue

            if actual == '{':
                code_stream = []
                actual = rules_stream.pop(0)

                while actual != '}':
                    code_stream.append(actual)
                    actual = rules_stream.pop(0)

                actual_rule.code = code_stream

                if actual_rule.rule != '':
                    self.tokenRules.append(actual_rule)
                else:
                    print('Lexical Error: rule has no token')

                actual_rule = Token()
                continue

            if actual in ["'", '"']:
                token_name = ['(']
                actual = rules_stream.pop(0)

                while actual not in ["'", '"']:
                    symbol = ord(actual)

                    if symbol not in self.alphabet:
                        self.alphabet.append(symbol)

                    token_name.append(symbol)
                    actual = rules_stream.pop(0)

                token_name.append(')')

                if actual_rule.rule != '':
                    print('Lexical Error: Bad definition of rule token')

                actual_rule.rule = token_name
                continue

            if actual == '(' and rules_stream[0] == '*':
                rules_stream.pop(0)

                actual = rules_stream.pop(0)
                lookAhead = rules_stream[0]
                founded_closing = False

                while not founded_closing:
                    if actual == '*' and lookAhead == ')':
                        founded_closing = True
                        rules_stream.pop(0)
                        continue

                    actual = rules_stream.pop(0)
                    lookAhead = rules_stream[0]

                continue

            else:
                token_name = [actual]
                actual = rules_stream.pop(0)

                while actual not in ['\t', ' ', '{']:
                    token_name.append(actual)
                    actual = rules_stream.pop(0)

                if actual == '{':
                    rules_stream.insert(0, actual)

                actual_rule.rule = self._recursive_expresion(token_name)

    def _process_token(self, token: list) -> str:
        ''' Devuelve le nombre del token '''
        token = token[1:] if token[0] == ' ' else token
        token = token[:-1] if token[-1] == ' ' else token
        return_stm, token_name = token.split(' ')
        return token_name

    def _firstCHarInLine(self, line):
        ''' Devuelve el primer caracter en la linea de texto '''
        if len(line) == 0:
            return 0
        line = list(line)
        actual = line.pop(0)

        while actual == ' ':
            actual = line.pop(0)

        return actual

    def _getDefinition(self, line: list) -> RegularDef:
        ''' Devuelve una definicion en base a la linea de codigo yalex '''
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
        ''' 
            Procesa una nueva regex 

            raw expresion: 
                - Expresion regular con definiciones nuevas

            recursive expression:
                - Definicion regular que utiliza definiciones
                  regulares definidas
        '''
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
        ''' Procesamiento de Expresiones regulares que utilizad definiciones pasadas '''

        # Definiciones pasadas
        og_regex = cp(regex)
        definitions = self.regexDefs
        regex_names = [regex.name for regex in definitions]
        starters = [regex[0] for regex in regex_names]
        out_regex = []

        # Escaneo de la regex
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

            # Simbolo de cualquier caracter
            if actual == ord('_'):
                expresions = []

                # Se utiliza del ASCII 32 al 126
                for ascii in range(32, 127):
                    expresions.append(ascii)
                    if ascii not in self.alphabet:
                        self.alphabet.append(ascii)

                out_regex = out_regex + self._toRegexOr(expresions)
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
        ''' Procesamiento de definiciones regulares nuevas '''
        expresions: list = []
        reading_exp: bool = False
        secuence_start = None
        secuence_end = None

        # Escaneo de Regex
        while len(regex) > 0:
            actual = ord(regex.pop(0))
            lookAhead = ord(regex[0]) if len(regex) > 0 else None

            # Cambio de estado
            if actual in [ord("'"), ord('"')]:
                reading_exp = not reading_exp
                if not reading_exp and secuence_start is not None:
                    secuence_end = expresions[-1]

            # Estado: Leer expresion
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

            # Inicio de secuencia
            if actual == ord('-') and not reading_exp:
                secuence_start = expresions[-1]

            # Inicio y final de secuencia encontrados
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

        # Manejo de errores
        if secuence_start is not None or reading_exp:
            regex = '[' + ''.join(regex) + ']'
            print('(Error Lexico) Expresion invalida:', regex)
            return regex

        return self._toRegexOr(expresions)

    def _toRegexOr(self, expresions: list) -> list:
        ''' Devuelve una regex que acepta cualquiera de las expresiones en (expresions)'''
        if len(expresions) == 1:
            if type(expresions[0]) == list:
                return expresions[0]

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

        for regex in self.ogDefs:
            string += '  -> '
            string += transformPostfix(regex[0])
            string += ' = '
            string += transformPostfix(regex[1])
            string += '\n'

        string += '\n---- Processed Definitions ----\n'

        for regex in self.regexDefs:
            string += '  -> '
            string += transformPostfix(regex.name)
            string += ' = '
            string += transformPostfix(regex.regex)
            string += '\n'

        string += '\n---- Rules ----\n'

        for token in self.tokenRules:
            string += '  -> '
            string += transformPostfix(token.rule)
            string += ' = '
            string += '{' + ''.join(token.code) + '}'
            string += '\n'

        string += '\n---- Final Regex ----\n'
        string += transformPostfix(self.unifiedRegex)
        string += '\n'

        return string

    def printFile(self):
        ''' Escribe el archivo ./out/steps.txt con el proceso de lectura YALex '''
        f = open('./out/steps.txt', 'w')
        f.write(self.__repr__())
        f.close()
