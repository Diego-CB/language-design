from copy import copy as cp
from .util import Item


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

    # Process Tokens and productions
    for line in tokenLines:
        if line[0] == 'TOKEN':
            new_tokens = _process_token(line[1])
            for token in new_tokens:
                tokens.append(token)

        elif line[0] == 'PRODUCTION':
            new_prod = _process_production(line[1])
            productions.update(new_prod)

    # Getting items out of productions
    prod_list: list[Item] = _itemsfromProd(productions)

    # Getting augmented grammar
    starting = prod_list[0].left
    start_item = Item('E\'', ['.', starting])
    last_item = Item('E\'', [starting, '.'])
    prod_list.append(last_item)
    prod_list.append(start_item)

    return tokens, prod_list


def _itemsfromProd(prod: dict) -> list[Item]:
    new_items_list: list[Item] = []

    for k in prod.keys():
        new_items = _getitems(prod[k])

        for item in new_items:
            new_item = Item(k, item)
            new_items_list.append(new_item)

    return new_items_list


def _getitems(prods) -> list:
    new_prods = []

    for prod in prods:
        for n in range(len(prod) + 1):
            og: list = cp(prod)
            og = og[:n] + ['.'] + og[n:] if n < len(og) else og + ['.']
            new_prods.append(og)

    return new_prods
