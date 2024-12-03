#!/usr/bin/env python3

import argparse
import re
import pdb

def parseLine(r,line):
    return sum([int(x) * int(y) for x,y in re.findall(r,line)])

def p2ParseLine(r,line):
    matches = re.findall(r,line)
    on = True
    ret = 0
    for match in matches:
        if match[2] == 'do': on = True;continue
        if match[3] == 'don': on = False; continue
        if on: ret += int(match[0])*int(match[1])

    return ret

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    rp1 = re.compile(r'mul\(([0-9]+),([0-9]+)\)')
    lines = []
    with open(args.filename,'r') as f:
        lines = f.readlines()
    p1 = 0
    for line in lines:
        p1 += parseLine(rp1,line)
    p2 = 0
    rp2 = re.compile(r'mul\(([0-9]+),([0-9]+)\)|(do)\(\)|(don)\'t\(\)')
    p2 = p2ParseLine(rp2,'\n'.join(lines))

    print(p1)
    print(p2)
