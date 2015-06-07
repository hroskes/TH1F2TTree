#No promises, but this worked for my case
#It's for converting an EDAnalyzer that makes a bunch of histograms
#into one that makes a tree.

import re, os, sys

def rreplace(s, old, new, count = -1):
    li = s.rsplit(old, count)
    return new.join(li)


try:
    infile = sys.argv[1]
except IndexError:
    raise IOError("Need to specify infile as command line argument")
try:
    outfile = sys.argv[2]
except IndexError:
    outfile = infile.replace(".cc", "_tree.cc")
if os.path.exists(outfile):
    raise IOError(outfile + " already exists!")

with open(infile) as inf, open(outfile, 'w') as outf:
    output = ""
    lastfillline = None
    definedtree = False
    initializedtree = False
    for line in inf:
        if line is None:
            break
        elif "#include " in line and "TH1F" in line:
            newline = line + line.replace("TH1F","TTree")
        elif re.match("^ *TH1F", line):
            if definedtree:
                newline = ""
            else:
                newline = "TTree *tree;\n"
                definedtree = True
            newline += line.replace("TH1F", "float").replace("*", "")
        elif "->make<TH1F>" in line:
            m = re.match('^( *)(\w+)'             #indentation and TH1F* variable name
                         '[ =]*\w*->make<TH1F>\(' #dont care about this
                          ' *"([^"]*)'            #histogram name
            , line)
            if initializedtree:
                newline = ""
            else:
                newline = line.replace(m.group(2), "tree").replace("make<TH1F>", "make<TTree>").split("(")[0] + '("tree", "tree");\n'
                initializedtree = True

            newline += m.group(1) + 'tree->Branch("' + m.group(3) + '", &' + m.group(2) + ");\n"

        elif "->Fill" in line:
            newline = line.replace("->Fill", " = ")
            lastfillline = newline
        else:
            newline = line

        output += newline

    output = rreplace(output, lastfillline, lastfillline + "\ntree->Fill();\n", 1)
    print infile.replace(".cc", "")
    output = output.replace(os.path.basename(infile).replace(".cc", ""), os.path.basename(outfile).replace(".cc", ""))
    outf.write(output)
