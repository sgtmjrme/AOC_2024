#!/usr/bin/env python3

import argparse
import pdb
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)

ninesHit: set

directions = [Point(1,0),Point(0,1),Point(-1,0),Point(0,-1)]

def inBounds(p: Point, maxX: int, maxY: int) -> bool:
    if p.x < 0: return False
    if p.x >= maxX: return False
    if p.y < 0: return False
    if p.y >= maxY: return False
    return True

def walkPath(table: 'list[list[int]]', point: Point, maxX, maxY, curVal: int):
    global directions
    global ninesHit
    mySum = 0
    if curVal == 9: 
        ninesHit.add(f'{point}')
        return 1
    nextVal = curVal + 1
    for dir in directions:
        newPoint = point + dir
        if not inBounds(newPoint,maxX,maxY): continue
        if table[newPoint.y][newPoint.x] == nextVal: 
            mySum += walkPath(table,newPoint,maxX,maxY, nextVal)
    return mySum

def printTable(table: 'list[list[int]]'):
    for y in range(len(table)):
        for x in range(len(table[y])):
            print(table[y][x],end='')
        print()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    p1 = 0
    p2 = 0
    string = ''
    table = []
    start0 = []
    with open(args.filename,'r') as f:
        for y,line in enumerate(f):
            table.append([int(i) if i!= '.' else '.' for i in line.strip()])
            for x,i in enumerate(table[-1]):
                if i == 0: start0.append(Point(x,y))
            maxY = y + 1
            maxX = len(table[-1])
    
    #Table is table[y][x]
    for point in start0:
        ninesHit = set()
        #p1 += walkPath(table,point,maxX,maxY,0)
        p2 += walkPath(table,point,maxX,maxY,0)
        p1 += len(ninesHit)

    
    print(p1)
    print(p2)
