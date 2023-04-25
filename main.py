from src import *
import sys

if __name__ == '__main__':

    # if len(sys.argv) < 2:
    #     raise Exception('Input Yalex File Missing')

    # filepath = sys.argv[1]

    filepath = './Examples/yalex/xd2.yal'
    ReadYalex(filepath=filepath)

# filepath = './Examples/slr-4.yal'
# filepath = './Examples/slr-1.yal'
# filepath = './Examples/xd.yal'
# filepath = './Examples/slr-2.yal'
# filepath = './Examples/xd2.yal'
