#!/usr/bin/python3

import string

def kill(inFilename, outFilename=''): 
    inFile = open(inFilename, 'r')

    if outFilename == '':
        outFilename = inFilename.replace('.', '_mod.')
    outFile = open(outFilename, 'w')

    for line in inFile:
        #line = line.rstrip('\r\n')
        #print('%s ... ' % line, end='')
        newLine = ''
        for char in line:
                if char in string.printable:
                        newLine += char
                else:
                        #print(char)
                        pass
        #print('%s\n' % newLine, end='')
        outFile.write(newLine)
    inFile.close()
    outFile.close()

if __name__=='__main__':
    import sys
    if len(sys.argv) == 3:
        try:
            kill(sys.argv[1], outFilename=sys.argv[2])
        except Exception as e:
            sys.stderr.write('Something went wrong: ' + e)
            quit()
    else:
        print('Usage: `killUnprintable.py infile outfile\'')
        quit()
