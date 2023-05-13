from copy import copy as cp


def _process_token(line: str) -> list[str]:
    line = line.replace('/n', '')
    line = line.replace('%token', '')
    tokens = [token for token in line.split(' ') if token != '']
    return tokens


def _process_production(line: str) -> list[str]:
    new_prod = {}
    line = line.replace('/n', '')
    line = line.replace('/', '')
    line = line.replace(';', '')
    prod_name, line = line.split(':')
    productions = line.split('|')
    new_prod[prod_name] = [_proces_partProd(p) for p in productions]
    return new_prod


def _proces_partProd(prod: str) -> list[str]:
    return [token for token in prod.split(' ') if token != '']


def processLines(tokenLines: list[str]) -> None:
    tokens: list = []
    productions: dict = {}

    for line in tokenLines:
        if line[0] == 'TOKEN':
            new_tokens = _process_token(line[1])
            for token in new_tokens:
                tokens.append(token)

        elif line[0] == 'PRODUCTION':
            new_prod = _process_production(line[1])
            productions.update(new_prod)

    print(tokens)
    productions = _itemsfromProd(productions)

    for p in productions.keys():
        print(p, '->', productions[p])


def _itemsfromProd(prod: dict) -> dict:
    new_items: dict = {}
    for k in prod.keys():
        new_items[k] = _getitems(prod[k])

    return new_items


def _getitems(prods):
    new_prods = []

    # TODO reemplazar insert con funcion custom que no reemplaze la data
    #      sino la mueva para poner el "."
    for prod in prods:
        for n in range(len(prod)):
            og: list = cp(prod)
            og.insert(n, '.')
            new_prods.append(og)

    return new_prods
