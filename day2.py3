#!/usr/bin/env python3

import argparse
import pdb

def line_ok(splits, safety = False):
    #If the input is less than 2 items, it's always good.  
    if len(splits) < 2: return True
    #If the first two values are the same
    if splits[1] == splits[0]:
        if safety: return line_ok(splits[1:]) #If we're being "safe", try again and remove the first value from the list
        return False #Otherwise, it's not correct
    inc = splits[1] > splits[0] #Find out whether we're increasing or decreasing

    
    for i,val in enumerate(splits):
        if i==0: continue #Skip the first iteration (because python always starts at the beginning of the list)
        splitdiff = splits[i]-splits[i-1] #Find the diff
        if (abs(splitdiff) > 0 and abs(splitdiff) < 4 and ((splitdiff > 0) == inc)): continue #Check for validity - between 1 and 3, and matches the expected direction.  
                                                                                              #This will continue through the end of the list if all is good
        if safety: #We are in "safety" mode, so we have to check sublists
            zeroly = False if i<=1 else line_ok(splits[0:i-2] + splits[i-1:]) #This checks against the pattern "3 4 3 2 1", where dropping the first value is necessary.  As such, only matters when i>1.
            firstly = True if i >= len(splits) else line_ok(splits[0:i-1] + splits[i:]) #Check the list dropping out the previous value
            if i+1==len(splits): return True #We were at the end 
            if i+1 > len(splits): pdb.set_trace() #We should never hit this
            lastly = line_ok(splits[0:i] + splits[i+1:]) #Check the list dropping out the current value
            return zeroly or firstly or lastly #If any of the above three lists (with various items removed) is OK, it passes.  
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
