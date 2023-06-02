from src import *
import sys
import os
from tabulate import tabulate

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Input Files Missing')

    # py ./main.py ./yalex/slr-1.yal ./yapar/slr-1.yalp ./input/1.txt

    # Lexical Analyzer Generator
    token_names = ReadYalex(filepath=sys.argv[1])
    # token_names = ReadYalex(filepath='./yalex/slr-1.yal')

    # Sintactic Analyzer Generator
    LR1, tokens_yapar = ReadYapar(
        filepath=sys.argv[2],
        token_names=token_names
    )
    # LR1, tokens_yapar = ReadYapar(filepath='./yapar/slr-1.yalp', token_names=token_names)

    # tokenization of input file
    os.system(f'py ./out/Scanner.py {sys.argv[3]}')
    # os.system('py ./out/Scanner.py ./input/1.txt')

    f = open('./out/tokens.txt', 'r')
    tokens = f.readlines()
    f.close()
    actual_tokens = []

    for token in tokens:
        temp = token
        temp = temp.replace('\'', '')
        temp = temp.replace(' ', '')
        temp = temp.replace('[', '')
        temp = temp.replace(']', '')
        temp = temp.replace('\n', '')
        temp = temp.split(',')
        actual_tokens.append(temp)

    tokens = [t[0] for t in actual_tokens]
    readed_tokens = [t for t in tokens if t in tokens_yapar]
    acc, iterations = LR1.simulate(readed_tokens)
    iterations_table = tabulate(
        iterations, headers=['STACK', 'INPUT', 'ACTION'],
        tablefmt='grid'
    )
    print('-----------------------------------------------------')
    print(f'-> Input Tokens {"NOT" if not acc else ""} ACCEPTED')
    print('-----------------------------------------------------')

    f = open("./out/actions.txt", "w")
    f.write(iterations_table)
    f.write(f'\n-> Input Tokens {"NOT" if not acc else ""} ACCEPTED\n')
    f.close()
    print('-> Actions table written in ./out/actions.txt')
