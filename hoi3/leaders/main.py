# -*- coding: <encoding name> -*-

def readfile(filename):
    with open(filename, 'rb') as input:
        content = input.read()
        input.close()
        return content.decode('gbk')

class Column(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def format(self, indent=0):
        s = ""
        s += str(self.key)
        s += " = "
        if type(self.val) is Struct:
            s += self.val.format(indent)
        else:
            s += str(self.val)
        return s

    def __str__(self):
        return self.format()

    def __repr__(self):
        return self.format()

    @staticmethod
    def decode(data):
        if type(data) is not dict:
            raise Exception("not a column")
        key = data['key']
        val = data['val']
        if type(val) is list:
            val = Struct.decode(val)
        return Column(key, val)

class Struct(object):
    def __init__(self, columns=[]):
        self.columns = columns

    def format(self, indent=0):
        s = ""
        s += "{\n"
        for c in self.columns:
            for i in range(indent + 1):
                s += "\t"
            s += c.format(indent + 1)
            s += "\n"
        for i in range(indent):
            s += "\t"
        s += "}"
        return s

    def __str__(self):
        return self.format()

    def __repr__(self):
        return self.format()

    def getcolumn(self, name):
        sel = None
        for c in self.columns:
            if c.key == name:
                if sel is not None:
                    raise Exception("multi columns.key = %s" % name)
                sel = c
        return sel

    @staticmethod
    def decode(data):
        if type(data) is not list:
            raise Exception("not a struct")
        ret = []
        for c in data:
            ret.append(Column.decode(c))
        return Struct(ret)

def restruct(data):
    if type(data) is not list:
        raise Exception("not a root")
    ret = []
    for c in data:
        ret.append(restruct_column(c))
    return ret

from parser import Parser

level1 = "♠ ♠ ✩ ✩ ✬ ✬ ✪ ✪ ✙ "
level2 = "① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ "

def getLevelStar(l, i):
    n = i * 2
    if n >= 0 and n < len(l):
        if l[n] != ' ':
            return l[n]
    raise Exception("out of range: level = '%s', len = %d, index = %d" % l, len(l), i)

def getLevel1(i):
    return getLevelStar(level1, i)

def getLevel2(i):
    return getLevelStar(level2, i)

if __name__ == "__main__":
    text = readfile("data/CHI.txt")
    data = Parser().parse(text)
    if type(data) is not list:
        raise Exception("not a conf data")
    conf = []
    for s in data:
        conf.append(Column.decode(s))

    for e in conf:
        level = e.val.getcolumn("max_skill")
        cname = e.val.getcolumn("name")
        s = cname.val[1:-1]
        cname.val = '"' + cname.val[1:-1] + getLevel1(int(level.val)) + '"'
        print(e)

    for i in range(0, 9):
        print(getLevel1(i), getLevel2(i))
