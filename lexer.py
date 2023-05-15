from src import *
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise Exception('Input Files Missing')

    # Lexical Analyzer Generator
    token_names = ReadYalex(filepath=sys.argv[1])
