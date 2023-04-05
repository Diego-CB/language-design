from drivers import *
from src import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input Yalex File Missing')

    # Read Input File
    filepath = sys.argv[1]
    reader: YalexReader = YalexReader(filename=filepath)
    print(reader)
