

def getRegex(charBuffer:list[list[str]]) -> list[str]:
    global definitions
    definitions = []

    for line in charBuffer:
        while len(line) > 0:
            actual = line.pop(0)
            lookAhead = line[0]

            # Handle delimeters
            if actual in [' ', '\n']:
                continue

            if actual == '\\' and lookAhead == 't':
                charBuffer.pop(0)
                continue

            # Handle Comments
            if actual == '(' and lookAhead == '*':
                line.pop(0)

                while actual != '*' and lookAhead == ')':
                    actual = line.pop(0)
                    lookAhead = line[0]

                line.pop(0)
                continue

            # Handle regular definitions
            if actual == 'l' and lookAhead == 'e' and line[2] == 't':
                line.pop(0)
                line.pop(0)
                line.pop(0)
                _getDefinition(line)
            
            # Ignore Productions
            if actual + lookAhead + line[2] + line[3] == 'rule':
                while len(line) > 0:
                    line.pop(0)

                continue

def _getDefinition(line):
    new_name = ''
    new_def = ''

    actualstring = new_name
    while len(line) > 0:


                




        

        


