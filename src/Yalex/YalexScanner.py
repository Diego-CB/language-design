import sys
from FileReader import getRegex

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input Yalex File Missing')

    # Read Input File
    filepath = sys.argv[1]
    file = open(filepath)
    lines = file.readlines()
    file.close()

    # Get ACII Buffer
    AciiBuffer:list = []
    charBuffer:list = []
    chars = []

    charBuffer = [
        [c for c in line]
            for line in lines
    ]

    # regex = getRegex(charBuffer)

    for line in charBuffer:
        if line
        print(line)
