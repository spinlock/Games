# -*- coding: <encoding name> -*-

def readfile(filename):
    with open(filename, 'rb') as input:
        content = input.read()
        input.close()
        return content.decode('gbk')

from parser import Parser

if __name__ == "__main__":
    text = readfile("data/leaders/CHI.txt")
    print (text[:200])
    p = Parser()
    p.settext(text)
    for i in range(20):
        t = p.token()
        if t == None:
            break
        print ("text %s" % t)
    print (p.parse(text))
