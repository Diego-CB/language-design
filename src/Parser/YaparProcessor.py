
class Prod:
    def __init__(self) -> None:
        self.name: None
        self.productions: None

    def __repr__(self) -> str:
        return f'{self.name} -> {self.productions}'


def processLines(tokenLines: list[str]) -> None:
    tokens: list = []
    productions: list = []

    for line in tokenLines:
        if line[0] == 'TOKEN':
            new_tokens = _process_token(line[1])
            for token in new_tokens:
                tokens.append(token)

        elif line[0] == 'PRODUCTION':
            new_prod = _process_production(line[1])
            productions.append(new_prod)

    print(tokens)

    for p in productions:
        print(p)


def _process_token(line: str) -> list[str]:
    line = line.replace('/n', '')
    line = line.replace('%token', '')
    tokens = [token for token in line.split(' ') if token != '']
    return tokens


def _process_production(line: str) -> list[str]:
    new_prod = Prod()
    line = line.replace('/n', '')
    line = line.replace('/', '')
    line = line.replace(';', '')
    prod_name, line = line.split(':')
    new_prod.name = (prod_name)
    productions = line.split('|')
    productions = [_proces_partProd(p) for p in productions]
    new_prod.productions = (productions)
    return new_prod


def _proces_partProd(prod: str) -> list[str]:
    return [token for token in prod.split(' ') if token != '']
