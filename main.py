from drivers import *
from src import *
import sys

if __name__ == '__main__':
    filepath = './Examples/slr-1.yal'
    reader: YalexReader = YalexReader(filename=filepath)
    print(reader)

else:
    if len(sys.argv) < 2:
        raise Exception('Input Yalex File Missing')

    # Read Input File
    filepath = sys.argv[1]
    reader: YalexReader = YalexReader(filename=filepath)
    print(reader)
