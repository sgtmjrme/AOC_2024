#!/usr/bin/env python3

import argparse
import math
import multiprocessing
import os
import pdb
from dataclasses import dataclass
import sys
import time

@dataclass
class Point:
    x: int
    y: int

    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)

    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)

def parseLine(line: str, y: int, d: 'dict[str][list[Point]]') -> None:
    for i,val in enumerate(line):
        if val == '.': continue
        if not val in d:
            d[val]=[]
        d[val].append(Point(i,y))

def inBounds(p: Point, maxX: int, maxY: int) -> bool:
    if p.x < 0: return False
    if p.x >= maxX: return False
    if p.y < 0: return False
    if p.y >= maxY: return False
    return True

def helper(queue: multiprocessing.Queue, results: multiprocessing.Queue, maxX, maxY, p1):
    global mymap
    while(not queue.empty()):
        #print(f'Queue length {queue.qsize()}')
        points = queue.get(timeout=1)
        if points == 'HELLO WORLD': 
            #print(f'Process {os.getpid()} exiting')
            sys.exit(0)
        l: 'list[Point]' = mymap[points]
        #Now do the actual work
        for i in range(len(l)):
            for j in range(len(l)):
                if i == j: continue
                diff = l[i] - l[j]
                curPoint = l[i] + diff
                while inBounds(curPoint,maxX,maxY):
                    results.put(curPoint)
                    if p1: break
                    curPoint = curPoint + diff

def doWork(maxX: int, maxY: int, p2 = False):
    queue = multiprocessing.Queue()
    results = multiprocessing.Queue()
    for points in mymap:
        queue.put(points)
    for _i in range(multiprocessing.cpu_count()):
        queue.put("HELLO WORLD")
    processes = [multiprocessing.Process(target=helper, args=(queue,results, maxX, maxY, not p2)) for x in range(multiprocessing.cpu_count())]
    print("Starting the processes!")
    for p in processes:
        p.start()

    print("Waiting on processes!")
    done = True
    while not done: 
        for p in processes:
            if p.is_alive(): done = False
            else: print(f'Joining {p}');p.join()
        time.sleep(1)
    print("Done waiting")

    antinodes = set()
    if p2: 
        for freq in mymap:
            for point in mymap[freq]:
                antinodes.add(f'{point}')
    while not results.empty():
        res = f'{results.get()}'
        antinodes.add(res)
    return len(antinodes)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    parser.add_argument('-d',help='Debug',default=False,action='store_true',dest='debug')
    args = parser.parse_args()

    global mymap
    global debug
    debug = args.debug
    mymap = {}
    with open(args.filename,'r') as f:
        #Read in the map
        for i,line in enumerate(f):
            parseLine(line.strip(), i, mymap)
        maxX = len(line)
        maxY = i + 1

    p1 = doWork(maxX,maxY)
    p2 = doWork(maxX,maxY,True)
    
    print(p1)
    print(p2)
