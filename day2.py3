#!/usr/bin/env python3

import argparse
import pdb

def line_ok(splits, safety = False):
    if len(splits) < 2: return True
    if splits[1] == splits[0]:
        if safety: return line_ok(splits[1:])
        return False
    inc = splits[1] > splits[0]

    #if splits[0] == 57 and splits[1] == 58: pdb.set_trace()
    for i,val in enumerate(splits):
        if i==0: continue
        splitdiff = splits[i]-splits[i-1]
        if (abs(splitdiff) > 0 and abs(splitdiff) < 4 and ((splitdiff > 0) == inc)): continue
        if safety: 
            zeroly = False if i<=1 else line_ok(splits[0:i-2] + splits[i-1:])
            firstly = True if i >= len(splits) else line_ok(splits[0:i-1] + splits[i:])
            if i+1==len(splits): return True #We were at the end
            if i+1 > len(splits): pdb.set_trace() #We should never hit this
            lastly = line_ok(splits[0:i] + splits[i+1:])
            return zeroly or firstly or lastly
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
            if line_ok(splits): safeLines += 1
            if line_ok(splits,True): safeP2Lines += 1;print(splits + ['Good'])
            else: 
                print(splits + ['Bad'])

    print(safeLines)
    print(safeP2Lines)
