#!/usr/bin/env python3

import argparse
import pdb
from dataclasses import dataclass, field


#The general idea of this code:
#A Row contains 3 values
#  The total - how many numbers will be in this row. This is only valid FOR THE ROW YOU'RE ON, not any future row
#  A list of length 10, telling you how many 0-9's there are (ex, [0,5,0,0,0,0,0,0,0] means there is 5 "1"'s)
#  Anything that isn't a number 0-9
#I differentiate these because most numbers will eventually fall into these, and they loop, so pre-compute loop values
#When pre-computing, I have a list of Rows saying how a number will affect all future rows. 
# Ex, 0 will go to 1, so its pre-computed row is only 1 long, Row(1,[0,1,0,...],{})
# 1 will be 3 rows long
#   Row(1,[0,0,...],{}) (2024)
#   Row(2,[0,0...],{}) (20 24)
#   Row(4,[1,0,2,0,1,...],{}) (2 0 2 4)
#For each blink, go through all #'s in the 0-9 list and add those future rows to a rolling buffer
# Then go through each non-0-9 and just compute those manually (I expected these to be small, they weren't necessarily)
# the total count on the row is the total number of #'s that will exist on that row.
# So when you get to the blink you want, your total is already pre-computed. 

#""" Combine two dicts together, so d1 includes all values from d2 """
def combineOtherToHandle(d1: 'dict[int]',d2: 'dict[int]'):
    for num in d1:
        d1[num] += d2[num] if num in d2 else 0
    for num in d2:
        if not num in d1 and d2[num] > 0: 
            d1[num] = d2[num]
    return d1

#"""One 'Blink' of time """
@dataclass
class Row:
    total: int = 0
    numOfNums: 'list[int]' = field(default_factory=list)
    otherToHandle: 'dict[int]' = field(default_factory=dict)

    def __add__(self,other: 'Row'):
        return Row(self.total + other.total,
                   [self.numOfNums[x] + other.numOfNums[x] for x in range(len(self.numOfNums))],
                   combineOtherToHandle(self.otherToHandle,other.otherToHandle)
                   )
    
    def __mul__(self,other: int): #Only works for scalars!
        out = Row().clear()
        out.total = self.total * other
        for i in range(len(self.numOfNums)):
            out.numOfNums[i] = self.numOfNums[i] * other
        for num in self.otherToHandle:
            out.otherToHandle[num] = self.otherToHandle[num] * other
        return out

    def clear(self):
        self.total = 0
        self.numOfNums = [0]*10
        self.otherToHandle = {}
        return self

#""" Used to calculate the next row based on the current row when precomputing 0-9 """
def alterNums(curVals: 'list[int]', newVals: 'list[int]',i: int):
    if curVals[i] == 0: newVals.append(1)
    elif len(str(curVals[i])) % 2 == 0: 
        strVal = str(curVals[i])
        lenStrVal = len(strVal)
        newVals.append(int(strVal[0:int(lenStrVal/2)]))
        newVals.append(int(strVal[int(lenStrVal/2):]))
    else:
        newVals.append(curVals[i]*2024)

specialVals = [0,1,2,3,4,5,6,7,8,9,32,77,26]

#Used to pre-compute 0-9.  Specifically, make the list of rows for each # based on the #'s returned by alterNums.  For 8 (special case), add in 32, 26, and 77
#The only reason 8 needs a special case is because it ends with 32772608, which split is 32 77 26 08 and then 3 2 7 7 2 6 8... the 0 goes away due to the problem statement.  
#So I just cut 8 off early and add those into the other directly.  
#In retrospect, I could have just put 16192 in there and had 8 lead to 3 2 7 7 2 6 16192... but oh vell.
def makeRows(i: int) -> 'list[Row]':
    global specialVals
    rows: 'list[Row]' = []
    curVals = [i]
    while True:
        newVals = []
        for j in range(len(curVals)):
            alterNums(curVals,newVals,j)
        curVals = newVals
        rows.append(Row(len(curVals),[curVals.count(j) for j in range(10)]))
        if all([x in specialVals for x in curVals]):
            #Handle special case for 8
            if i == 8:
                for x in [32,26,77]: 
                    rows[-1].otherToHandle[x] = 1
            break
    return rows

#Yay debugging.
def printBuffer(buffer: 'list[Row]',bufPos = 0):
    bufferLen = len(buffer)
    print(f'----------- CURRENT BUFFER {bufPos % bufferLen} - {bufPos} -----------------')
    for i,row in enumerate(buffer):
        print(f'{">" if i%bufferLen == bufPos else ""}{row}')

#The check used after splitting the other list, to determine if it gets put back in other or added to the 0-9 list
def addNumToRowOrOther(num: int, row: Row):
    if num < 10: row.numOfNums[num] += 1
    elif num in row.otherToHandle: row.otherToHandle[num] += 1
    else: row.otherToHandle[num] = 1
    return row

#Parses otherToHandle.  The first if should never be hit.  Oh vell.  Multiplies/splits as the problem statement requires. 
def parseOtherToHandle(num: int) -> Row:
    if num == 0: return Row(1,[0,1,0,0,0,0,0,0,0])
    elif len(str(num)) % 2 == 0: 
        strVal = str(num)
        lenStrVal = len(strVal)
        v1 = int(strVal[0:int(lenStrVal/2)])
        v2 = int(strVal[int(lenStrVal/2):])
        ret = Row(2,[0]*10)
        addNumToRowOrOther(v1,ret)
        addNumToRowOrOther(v2,ret)
        return ret
    else:
        return addNumToRowOrOther(num*2024,Row(1,[0]*10))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File",required=True)
    parser.add_argument('-n',help='Number of blinks',dest='blinks',type=int,required=True)
    args = parser.parse_args()

    #Prep the 0-9 pre-compute list.
    singleDigitPrecompute: 'list[list[Row]]' = []
    for i in range(10):
        singleDigitPrecompute.append(makeRows(i))

    #Prep the rolling buffer
    bufferLen = max([len(x) for x in singleDigitPrecompute]) + 2
    buffer: 'list[Row]' = []
    for r in range(bufferLen):
        buffer.append(Row().clear())

    #Read input and load data into the buffer
    with open(args.filename,'r') as f:
        for i in [int(x) for x in f.readline().split()]:
            if not i in buffer[0].otherToHandle:
                buffer[0].otherToHandle[i] = 1
            else: buffer[0].otherToHandle[i] += 1
        buffer[0].total = len(buffer[0].otherToHandle)
    
    largestOther = 0 #Keeps track of the largest non-0-9 length.  Because I was interested.  Not needed for the code to work.
    resultRow: 'Row|None' = None
    for i in range(args.blinks):
        #Clean up the now unused buffer row since it's behind us.  
        buffer[(i-1)%bufferLen].clear()
        #For each of 0-9
        for j,rows in enumerate(singleDigitPrecompute):
            #Apply rows to the buffer row
            for k,row in enumerate(rows):
                # i is number of blinks
                # j is the digit I'm looking at
                # k is the row addition I'm making
                #Yay modulo arithmatic.  
                tmp = (i+k+1)%bufferLen
                buffer[tmp] += (row * buffer[i%bufferLen].numOfNums[j])
        #Handle everything that's not 0-9
        for j in buffer[i%bufferLen].otherToHandle:
            parsed = parseOtherToHandle(j)
            buffer[(i+1)%bufferLen] += parsed * buffer[i%bufferLen].otherToHandle[j]
        #Just set the output to the row we want, because I'm lazy and don't want to keep track of the last row outside this for loop.
        resultRow = buffer[(i+1)%bufferLen]
        largestOther = max(largestOther,len(resultRow.otherToHandle))
    printBuffer(buffer,args.blinks)
    if resultRow !=  None:
        print(resultRow.total)
        print(f'The largest size of the otherToHandle was {largestOther}')
    else:
        print('Wah wahhh')

#How the hell was I supposed to do this with recursion???