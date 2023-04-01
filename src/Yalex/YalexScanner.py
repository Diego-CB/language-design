import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Input Yalex File Missing')
    
    # Read Input File
    filepath = sys.argv[1]
    file = open(filepath)
    lines = file.readlines()
    file.close()

    # Get ACII Buffer
    buffer = []
    for line in lines:
        for c in line:
            buffer.append(ord(c))

    print(buffer)        
