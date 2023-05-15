from src import *
import sys

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     raise Exception('Input yapl File Missing')

    # filepath = sys.argv[1]
    filepath = './Examples/yapar/slr-1.yalp'

    ReadYapar(filepath=filepath)
