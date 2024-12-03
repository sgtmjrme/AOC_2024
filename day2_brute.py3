#!/usr/bin/env python3

import argparse
import pdb

def line_ok(splits, safety = False):
    if len(splits) < 2: return True
    if splits[1] == splits[0]:
        if safety: return line_ok(splits[1:])
        return False
    inc = splits[1] > splits[0]
    for i,val in enumerate(splits):
        if i==0: continue
        splitdiff = splits[i]-splits[i-1]
        if (abs(splitdiff) > 0 and abs(splitdiff) < 4 and ((splitdiff > 0) == inc)): continue
        return False
    return True

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-f','--file',dest='file')
    args = ap.parse_args()
    safeLines = 0
    safeP2Lines = 0
    with open(args.file,'r') as f:
        for line in f:
            splits = [int(x) for x in line.split()]
            if len(splits) < 1: continue
            if line_ok(splits): safeLines+=1
            ok = 0
            for i in range(len(splits)):
                ok += line_ok(splits[0:i]+splits[i+1:])
            if ok>0: safeP2Lines+=1
    print(safeLines)
    print(safeP2Lines)
