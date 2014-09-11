# -*- coding: <encoding name> -*-

def readfile(filename):
    with open(filename, 'rb') as input:
        content = input.read()
        input.close()
        return content.decode('gbk')

class Entry:
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def format(self, indent):
        s = ""
        for i in range(indent):
            s += "\t"
        s += str(self.key)
        s += " = "
        if type(self.val) is Group:
            s += self.val.format(indent)
        else:
            s += str(self.val)
            s += "\n"
        return s

    def __str__(self):
        return self.format(0)

    def __repr__(self):
        return self.format(0)

from collections import OrderedDict

class Group:
    def __init__(self, entries=[]):
        self.entries = OrderedDict()
        for e in entries:
            self.entries[e.key] = e.val

    def __getattr__(self, key):
        val = self.entries[key]
        if val is None:
            raise Exception("key = '%s' not found" % key)
        return val

    def __setattr_(self, key, val):
        self.entries[key] = val

    def format(self, indent, expand=True):
        s = ""
        s += "{\n"
        for key in self.entries:
            for i in range(indent + 1):
                s += "\t"
            s += key
            s += " = "
            val = self.entries[key]
            if type(val) is Group:
                s += val.format(indent + 1)
            else:
                s += str(val)
                s += "\n"
        for i in range(indent):
            s += "\t"
        s += "}\n"
        return s

    def __str__(self):
        return self.format(0)

    def __repr__(self):
        return self.format(0)

def restruct_entry(data):
    if type(data) is not dict:
        raise Exception("not a entry")
    key = data['key']
    val = data['val']
    if type(val) is not list:
        return Entry(key, val)
    else:
        return Entry(key, restruct_group(val))

def restruct_group(data):
    if type(data) is not list:
        raise Exception("not a group")
    ret = []
    for e in data:
        ret.append(restruct_entry(e))
    return Group(ret)

def restruct(data):
    if type(data) is not list:
        raise Exception("not a root")
    ret = []
    for e in data:
        ret.append(restruct_entry(e))
    return ret

from parser import Parser

stars = "✩ ✩ ✬ ✬ ✿ ✿ ❀ ❀ ✙"

if __name__ == "__main__":
    text = readfile("data/CHI.txt")
    p = Parser()
    root = restruct(p.parse(text))
    for e in root:
        print(e)
        print(e.val.max_skill)
    for s in stars:
        print(s)
