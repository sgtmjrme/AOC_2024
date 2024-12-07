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

    def __mul__(self,other):
        return Point(self.x*other.x,self.y*other.y)

@dataclass
class Line:
    start: 'Point'
    end: 'Point'

def minOfLine(line: Line):
    return Point(min(line.start.x,line.end.x),min(line.start.y,line.end.y))

def maxOfLine(line: Line):
    return Point(max(line.start.x,line.end.x),max(line.start.y,line.end.y))

def line_length(line: Line) -> int:
    return abs(line.start.x-line.end.x) + abs(line.start.y-line.end.y) + 1

def lines_intersect(line1: Line, line2: Line):
    maxesl1 = maxOfLine(line1)
    minsl1 = minOfLine(line1)
    maxesl2 = maxOfLine(line2)
    minsl2 = minOfLine(line2)
    if minsl2.x > maxesl1.x: return False
    if maxesl2.x < minsl1.x: return False
    if minsl2.y > maxesl1.y: return False
    if maxesl2.y < minsl1.y: return False
    return True

#Not necessary?
def lines_point_intersect(line: Line, point: Point):
    if line.start.x > point.x: return False
    if line.end.x < point.x: return False
    if line.start.y > point.y: return False
    if line.end.y < point.y: return False
    return True

def findNextStop(point: Point, direction: Point, walls: 'list[Point]') -> Point:
    dist = (math.inf, None)
    for wall in walls:
        if direction.x != 0: #We're in the X direction
            if wall.y != point.y: continue #But Y are different, so no need to check
            #So we're on the same X line
            d = wall.x - point.x
            absd = abs(d)
            if not d/absd == direction.x: continue #Wrong direction
            if absd > dist[0]: continue #No need to do any more checking if it's further
            #Ok, at this point we have a new valid point
            dist = (absd,wall)
        elif direction.y != 0: #Moving in the Y direction
            if wall.x != point.x: continue #X are different, no need to check
            #So we're on the same Y line.  
            d = wall.y-point.y
            absd = abs(d)
            if not d/absd == direction.y: continue #Wrong direction
            if absd > dist[0]: continue #No need to do any more checking if it's further
            #Ok, at this point we have a new valid point
            dist = (absd,wall)
    if dist[1] == None: return None
    return dist[1] - direction

def parseLine(line: str) -> 'tuple[int,list[int]]':
    global maxX
    start = -1
    walls = []
    for i,char in enumerate(line):
        if char == '^': start = i
        if char == '#': walls.append(i)
        maxX = i
    return (start,walls)

def genPath(start_pos,allWalls):
    global maxX
    global maxY
    ret = 0
    lines = [] 
    endpoints_hit = {}
    done = False
    directions = [Point(0,-1),Point(1,0),Point(0,1),Point(-1,0)]
    cur_direction = -1
    cur_pos = start_pos
    while not done:
        cur_direction+=1
        newBegin = cur_pos
        cur_pos = findNextStop(cur_pos,directions[cur_direction%4],allWalls)
        if cur_pos == None: 
            #We escaped!
            direction = directions[cur_direction % 4]
            cur_pos = Point(
                newBegin.x if direction.x == 0 else (0 if direction.x < 0 else maxX),
                newBegin.y if direction.y == 0 else (0 if direction.y < 0 else maxY)
                )
            done=True
        pos_dir_str = f'{cur_pos}:{directions[cur_direction % 4]}'
        if pos_dir_str in endpoints_hit: raise Exception
        endpoints_hit[pos_dir_str] = None
        newLine = Line(newBegin,cur_pos)
        ret += line_length(newLine)
        for line in lines:
            if lines_intersect(line,newLine): ret -= 1
        lines.append(newLine)
    return ret, lines

def p2Helper(queue: multiprocessing.Queue, results: multiprocessing.Queue, start_pos,  allWalls):
    while(not queue.empty()):
        print(f'Queue length {queue.qsize()}')
        line: Line = queue.get(timeout=1)
        if line == 'HELLO WORLD': 
            print(f'Process {os.getpid()} exiting')
            sys.exit(0)
        mins = minOfLine(line)
        maxes = maxOfLine(line)
        for x in range(mins.x,maxes.x+1):
            for y in range(mins.y, maxes.y+1):
                if Point(x,y) == start_pos: continue
                try:
                    genPath(start_pos,allWalls + [Point(x,y)])
                except:
                    results.put(Point(x,y))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    global maxX
    global maxY
    start_pos = (-1,-1)
    allWalls = []
    with open(args.filename,'r') as f:
        #Read in the map
        for i,line in enumerate(f):
            start,walls = parseLine(line)
            if start >= 0: start_pos = Point(start,i)
            if len(walls) > 0:
                allWalls.extend([Point(x,i) for x in walls])
                #allWalls[i] = {};[allWalls[i][x] = None for x in walls]
            maxY = i

    p1, lines = genPath(start_pos,allWalls)
    print(len(lines))
    p2 = 0
    queue = multiprocessing.Queue()
    results = multiprocessing.Queue()
    for line in lines:
        queue.put(line)
    for i in range(multiprocessing.cpu_count()):
        queue.put("HELLO WORLD")
    processes = [multiprocessing.Process(target=p2Helper, args=(queue,results,start_pos,allWalls)) for x in range(multiprocessing.cpu_count())]
    print("Starting the processes!")
    for p in processes:
        p.start()

    print("Waiting on processes!")
    jobnum=1
    done = True
    for p in processes:
        if p.is_alive(): done = False
        else: print(f'Joining {p}');p.join()
        time.sleep(1)
    print("Done waiting")

    points_hit = {}
    while not results.empty():
        res = f'{results.get()}'
        if res in points_hit: continue
        points_hit[res] = None
        p2+=1
    
    #I'm lazy on part 2, just re-run the above.

    print(p1)
    print(p2)
