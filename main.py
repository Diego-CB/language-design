from src import *
import sys
import os

if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     raise Exception('Input Files Missing')

    # py ./main.py ./yalex/slr-1.yal ./yapar/slr-1.yalp ./input/1.txt

    # Lexical Analyzer Generator
    token_names = ReadYalex(filepath=sys.argv[1])
    # token_names = ReadYalex(filepath='./yalex/slr-1.yal')

    # Sintactic Analyzer Generator
    ReadYapar(filepath=sys.argv[2], token_names=token_names)
    # ReadYapar(filepath='./yapar/slr-1.yalp', token_names=token_names)

    # tokenization of input file
    os.system(f'py ./out/Scanner.py {sys.argv[3]}')
    # os.system('py ./out/Scanner.py ./input/1.txt')
