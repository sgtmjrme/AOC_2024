#!/usr/bin/env python3

import argparse
import re
from functools import cmp_to_key
import pdb

global compareDict

def compare(val1,val2):
    global compareDict
    if val2 in compareDict:
        return -1 if val1 in compareDict[val2] else 1
    return 1


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()
    p1 = 0
    p2 = 0

    compareDict={}
    with open(args.filename,'r') as f:
        #Read in the rules
        while(line := f.readline()):
            line = line.strip()
            if line == '':
                break
            splits = line.split('|')
            if not splits[1] in compareDict:
                compareDict[splits[1]] = {}
            compareDict[splits[1]][splits[0]] = None
            #Rule format is Rule[later][earlier]
        
        while(line := f.readline()):
            splits = line.strip().split(',')
            sortedSplits = sorted(splits,key=cmp_to_key(compare))
            #If the two lists are the same, then there was no correction necessary
            if splits == sortedSplits: p1 += int(splits[int(len(splits)/2)])
            #If the two lists are different, the sorted list is now correct
            else: p2 += int(sortedSplits[int(len(sortedSplits)/2)])

    print(p1)
    print(p2)
