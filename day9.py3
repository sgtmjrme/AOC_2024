#!/usr/bin/env python3

import argparse
import pdb
from dataclasses import dataclass

@dataclass
class Item:
    count: int
    id: int
    isBlank: bool = True

def combineBlanks(splits: 'list[Item]'):
    i = len(splits)-1
    while(i > 1):
        if splits[i].isBlank and splits[i-1].isBlank:
            splits[i-1].count += splits[i].count
            splits.pop(i)
        i -= 1

def printSplits(splits: 'list[Item]'):
    for item in splits:
        char = '.' if item.isBlank else str(item.id)
        print(char*item.count,end='')
    print()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    p1 = 0
    p2 = 0
    string = ''
    with open(args.filename,'r') as f:
        string = f.readline().strip()

    splits = [int(x) for x in string]    
    if len(splits) % 2: splits.append(0)
                    
    #p1
    curPos = 0
    while splits[-2] <= 0: splits = splits[0:-2]
    for i in range(int(len(splits)/2)): #This range is really the max - we likely won't hit it
        if i >= len(splits)/2:break #Stop if we went past bounds because we don't recalculate the range above
        v1 = splits[i*2]
        for j in range(v1): 
            p1 += curPos * i
            curPos+=1
        v2 = splits[i*2+1]
        for j in range(v2):
            if len(splits)-1 <= (i*2+1):break #Stop if we have nothing more to move
            p1 += (len(splits)/2-1) * curPos
            curPos += 1
            splits[-2] -= 1
            if splits[-2] <= 0: splits = splits[0:-2]

    #p2
    splits = [int(x) for x in string]    
    if len(splits) % 2: splits.append(0)
    splits = [Item(x,int(i/2), i%2) for i,x in enumerate(splits)]
    curPos = 0
    while splits[-2].count <= 0: splits = splits[0:-2]
    lastPointer = len(splits)
    while lastPointer > 0:
        lastPointer -= 1
        if splits[lastPointer].isBlank: continue
        for pos in range(len(splits)):
            if pos > lastPointer: break
            if splits[pos].isBlank and splits[pos].count >= splits[lastPointer].count:
                #Fill it in
                emptyPos = splits[pos]
                splits[pos]=splits[lastPointer]
                splits[lastPointer] = Item(splits[pos].count,0)
                splits.insert(pos+1,Item(emptyPos.count-splits[pos].count,0))
                combineBlanks(splits)
                break

    curPos = 0
    for item in splits:
        if not item.isBlank:
            for _i in range(item.count):
                p2 += item.id * curPos
                curPos += 1
        else:
            curPos += item.count
    
    print(p1)
    print(p2)
