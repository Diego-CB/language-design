from src import *
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input Yalex File Missing')

    filepath = sys.argv[1]

    ReadYalex(filepath=filepath)
