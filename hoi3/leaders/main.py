# -*- coding: utf-8 -*-

class Column(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def format(self, indent=0, end="\n"):
        s = ""
        s += str(self.key)
        s += " = "
        if type(self.val) is Struct:
            s += self.val.format(indent, end)
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

    def format(self, indent=0, end="\n"):
        s = ""
        s += "{"
        s += end
        for c in self.columns:
            for i in range(indent + 1):
                s += "\t"
            s += c.format(indent + 1, end)
            s += end
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
import os

star1 = "☒ ☒ ✩ ✩ ✬ ✬ ✪ ✪ ✙ ✙ "
star2 = "① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ "

def level2star(i, text=star2):
    n = (i - 1) * 2
    if n >= 0 and n < len(text):
        s = text[n]
        if s != ' ':
            return s
    raise Exception("out of range: star = '%s', len = %d, index = %d" % (text, len(text), i))

def load(filename):
    with open(filename, 'rb') as input:
        text = input.read()
        text = text.decode('gbk')
        input.close()
    data = Parser().parse(text)
    if type(data) is not list:
        raise Exception("not a conf data")
    conf = []
    for s in data:
        conf.append(Column.decode(s))
    return conf

def store(filename, conf):
    d = os.path.dirname(filename)
    if not os.path.isdir(d):
        os.makedirs(d)
    text = ""
    for c in conf:
        text += c.format(end="\r\n")
        text += "\r\n"
    f = open(filename, 'wb+')
    f.write(text.encode('gbk'))
    f.close()

if __name__ == "__main__":
    for path, dirs, files in os.walk("data/"):
        for f in files:
            src = os.path.join(path, f)
            dst = os.path.join("output", src)
            print("%s -> %s" % (src, dst))
            conf = load(src)
            for e in conf:
                level = e.val.getcolumn("max_skill")
                cname = e.val.getcolumn("name")
                s = cname.val[1:-1]
                cname.val = "\"{1:s}{0:s}\"".format(cname.val[1:-1], level2star(int(level.val)))
            store(dst, conf)
            
    for i in range(1, 10):
        print(level2star(i, star1), level2star(i, star2))

