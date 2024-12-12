#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import pdb

def addArea(areaCnt: 'list[int]', c: str):
    areaCnt[ord(c[0])-65] += 1

def addFence(lineCnt: 'list[int]', c1: str, c2: 'str|None' = None):
    lineCnt[ord(c1[0])-65] += 1
    if c2: lineCnt[ord(c2[0])-65] += 1

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

@dataclass
class Char:
    char: 'str'
    isGrouped: bool = False
    isP2Used: bool = False

def inBounds(point: Point, maxX: int, maxY: int):
    if point.x < 0: return False
    if point.y < 0: return False
    if point.x >= maxX: return False
    if point.y >= maxY: return False
    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    p1 = 0
    p2 = 0
    prevLine = None
    line = ''
    cnt = 0
    areaCnt = [0]*26
    lineCnt = [0]*26
    table: 'list[list[Char]]' = []
    with open(args.filename,'r') as f:
        for line in f:
            table.append([])
            for c in line.strip():
                table[-1].append(Char(c))
    
    maxX = len(table[0])
    maxY = len(table)
    pdb.set_trace()

    dirs = [Point(0,1),Point(1,0),Point(-1,0),Point(0,-1)]
    score = 0
    for y in range(maxY):
        for x in range(maxX):
            if table[y][x].isGrouped: continue
            totFences = 0
            totArea = 0
            p2FenceReduction = 0
            toProcess = [Point(x,y)]
            processedPoints = []
            while len(toProcess) > 0:
                totArea += 1
                curPoint = toProcess.pop()
                processedPoints.append(curPoint)
                table[curPoint.y][curPoint.x].isGrouped = True
                #P1 processing
                for dir in dirs:
                    newPoint = curPoint + dir
                    if newPoint.x < 0 or newPoint.y < 0: totFences += 1;continue
                    if newPoint.x >= maxX or newPoint.y >= maxY: totFences += 1;continue
                    if table[curPoint.y][curPoint.x].char != table[newPoint.y][newPoint.x].char:
                        totFences += 1
                        continue
                    elif not table[newPoint.y][newPoint.x].isGrouped:
                        table[newPoint.y][newPoint.x].isGrouped = True
                        toProcess.append(newPoint)
                #P2 processing
                for x1 in [1,-1]:
                    for y1 in [1,-1]:
                        #I'm at a diagonal - setup for checks
                        numSameNeighbor = 0
                        hits = 0
                        dir = None
                        #Check Y
                        if inBounds(curPoint + Point(0,y1),maxX,maxY):
                            #In bounds, are we incrementing hit?
                            if table[curPoint.y][curPoint.x].char == table[curPoint.y + y1][curPoint.x].char:
                                hits += 1 #Yes, we are
                                dir = Point(0,y1)
                        #Check X
                        if inBounds(curPoint + Point(x1,0),maxX,maxY):
                            #In bounds, are we incrementing hit?
                            if table[curPoint.y][curPoint.x].char == table[curPoint.y][curPoint.x + x1].char:
                                hits += 1 #Yes, we are
                                dir = Point(x1,0)
                        if hits == 1: #We're in a line - but is the diagonal OK?
                            newPoint = curPoint + dir
                            #Have we taken account of this piece yet?
                            if not table[newPoint.y][newPoint.x].isP2Used:
                                #We haven't used this piece yet, so is the diagonal OK?
                                newPoint = curPoint + Point(x1,y1)
                                if inBounds(newPoint,maxX,maxY):
                                    #Is the point the same?
                                    if table[curPoint.y][curPoint.x].char == table[newPoint.y][newPoint.x].char:
                                        #It is... so do nothing
                                        pass
                                    else: 
                                        p2FenceReduction -= 1
                                else: p2FenceReduction -= 1
                table[curPoint.y][curPoint.x].isP2Used = True
            p1 += totFences * totArea
            p2 += (totFences + p2FenceReduction) * totArea


    
    print(p1)
    print(p2)