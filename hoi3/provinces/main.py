# -*- coding: <encoding name> -*-

def readfile(filename):
    with open(filename, 'rb') as input:
        content = input.read()
        input.close()
        return content.decode('gbk')

if __name__ == "__main__":
    content = readfile("province_names.csv")
    lines = []
    for l in content.splitlines():
        if len(l) == 0:
            continue
        lines.append(l)
    print(len(lines))
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
        print(l, tag, name)
        print("%s;%s;%s" %(tag, rename, l[idx2+1:]))
