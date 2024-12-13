#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import pdb
import re

@dataclass
class Button:
    x: int
    y: int

    def __init__(self,tup,y = None):
        if y != None: 
            self.x = int(tup);self.y = int(y)
        else:
            self.x = int(tup[0][0])
            self.y = int(tup[0][1])

@dataclass
class Prize:
    x: int
    y: int

    def __init__(self,tup,y = None):
        if y != None: 
            self.x = int(tup);self.y = int(y)
        else:
            self.x = int(tup[0][0])
            self.y = int(tup[0][1])

    def __add__(self, other: int):
        return Prize(self.x + other, self.y+other)
    
def findColinearSolution(buttons: 'list[Button]', prize: Prize):
    print("colinear!")
    print(buttons)
    print(prize)
    pdb.set_trace()

def calcButtonPresses(buttons: 'list[Button]',prize: Prize) -> 'tuple[int,int]':
    #Check of co-linear
    if (buttons[0].y/buttons[0].x == buttons[1].y/buttons[1].x):
        #Special case - they're colinear, so there can be multiple solutions.
        findColinearSolution(buttons,prize)
    but2Press = round((prize.y-((buttons[0].y*prize.x))/buttons[0].x)/(buttons[1].y-(buttons[0].y*buttons[1].x/buttons[0].x)))
    but1Press = round((prize.x - (buttons[1].x * but2Press))/buttons[0].x)
    return (but1Press,but2Press)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    p1 = 0
    p2 = 0
    butRe = re.compile(r'Button [AB]: X\+([0-9]+), Y\+([0-9]+)')
    prizeRe = re.compile(r'Prize: X=([0-9]+), Y=([0-9]+)')
    with open(args.filename,'r') as f:
        buttons: 'list[Button]' = []
        prize = None
        cnt = -1
        for line in (l.strip() for l in f):
            cnt += 1
            if cnt % 4 == 3: buttons = [];continue #Empty line
            if cnt % 4 < 2: buttons.append(Button(butRe.findall(line)));continue
            prize = Prize(prizeRe.findall(line))
            prize2 = prize + 10000000000000
            #print(buttons)
            #print(prize)


            #P1
            print(buttons)
            (but1Press,but2Press) = calcButtonPresses(buttons,prize)
            if but1Press <= 100 and but2Press <= 100:
                if buttons[0].y * but1Press + buttons[1].y * but2Press == prize.y: 
                    #We have a valid solution
                    cost = but1Press * 3 + but2Press
                    p1 += cost
            
            #P2
            print(buttons)
            (but1Press,but2Press) = calcButtonPresses(buttons,prize2)
            if buttons[0].y * but1Press + buttons[1].y * but2Press == prize2.y: 
                #We also have to re-check the X because of float shenanigans
                if buttons[0].x * but1Press + buttons[1].x * but2Press == prize2.x: 
                    #We have a valid solution
                    cost = but1Press * 3 + but2Press
                    p2 += cost
    
    print(p1)
    print(p2)