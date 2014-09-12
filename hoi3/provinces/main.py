# -*- coding: utf-8 -*-

import os

def load(filename):
    with open(filename, 'rb') as input:
        text = input.read()
        text = text.decode('gbk')
        input.close()
    lines = []
    for l in text.splitlines():
        if len(l) == 0:
            continue
        lines.append(l)
    return lines

def store(filename, lines):
    d = os.path.dirname(filename)
    if not os.path.isdir(d):
        os.makedirs(d)
    text = ""
    for l in lines:
        text += l
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
            lines = load(src)
            results = []
            for l in lines:
                idx1 = l.index(';')
                idx2 = l.index(';', idx1+1)
                tag = l[:idx1]
                if not tag.startswith("PROV"):
                    results.append(l)
                    continue
                name = l[idx1 + 1:idx2]
                rename = "P%05d.%s" % (int(tag[4:]), name)
                results.append("%s;%s;%s" %(tag, rename, l[idx2+1:]))
            store(dst, results)
