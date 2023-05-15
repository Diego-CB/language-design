from src import *
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('Input Files Missing')

    # Lexical Analyzer Generator
    token_names = ReadYalex(filepath=sys.argv[1])

    # Sintactic Analyzer Generator
    ReadYapar(filepath=sys.argv[2], token_names=token_names)

    # tokenization of input file
    os.system(f'py ./out/Scanner.py {sys.argv[3]}')
