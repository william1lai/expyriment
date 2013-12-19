#! /usr/local/cs/bin/python

"""
    transformer.py < [filename] - makes a file called
        'renamethisfile.cpp' that makes a template out
        of all of the function interfaces in a class

    Arguments: None. All input is taken from stdin.
"""

from sys import stdin
import re


def main():
    f = open('renamethisfile.cpp', 'w');
    line = stdin.readline()
    while not(re.search("^ *class ([^ ]*)$", line)):
        #print "Not a class declaration"
        line = stdin.readline()

    clsName = re.search("^class ([^ \n\r]*)", line).group(1)
    #print clsName

    line = stdin.readline()

    while line != "":
        while not (re.search("[^\t]*\(.*\)[^;]*;", line)):
            line = stdin.readline()
            #print line
            if line == "":
                return 0; #reached EOF
    
        if (re.search("= *0;$", line)):
            line = stdin.readline()
            continue
  
        virt = re.search("virtual ", line);
        if virt == None:
            virtIndex = 0
        else:
            virtIndex = virt.end()
        sig = re.search("[^\t]*\(.*\).*;", line).group()[virtIndex:-1]

        deParam = re.search("\(.*[A-Za-z0-9_]+( *= *.*)\)", sig)
        if deParam != None:
            deParamBeg = deParam.start(1)
            deParamEnd = deParam.end(1)
            sig = sig[:deParamBeg] + sig[deParamEnd:]
  
        #print sig
        splt = re.search("[A-Za-z0-9_]+ *\(", sig)
        if splt == None:
            splitIndex = 0
        else:
            splitIndex = splt.start()
        sigFirst = sig[:splitIndex]
        sigLast = sig[splitIndex:]

        #print sigFirst
        #print sigLast
        impl = sigFirst + clsName + "::" + sigLast + "\n{\n\n}\n\n"
        #print impl
        f.write(impl);
        line = stdin.readline()
        
    f.close()
    return 0


if __name__ == "__main__":
    main()
