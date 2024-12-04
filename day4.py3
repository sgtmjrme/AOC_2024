#!/usr/bin/env python3

import argparse
import re
import pdb

def print_table():
    for y in table:
        print(y)

def checkXMAS(M,A,S):
    global table
    if table[M[0]][M[1]] != 'M': return False
    if table[A[0]][A[1]] != 'A': return False
    if table[S[0]][S[1]] != 'S': return False
    return True

def P2Valid(y,x):
    global table
    for tup in [('S','M'),('M','S')]:
        if table[y-1][x-1] == tup[0] and table[y+1][x+1] == tup[1]:
            #We're good
            break
    else:
        return False
    for tup in [('S','M'),('M','S')]:
        if table[y+1][x-1] == tup[0] and table[y-1][x+1] == tup[1]:
            #We're good
            break
    else:
        return False
    return True

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    #Load data
    global table
    table = []
    with open(args.filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            table.append(line.strip())
    print_table()
    p1 = 0
    p2 = 0

    table_length = len(table)
    t_check_length = table_length - 3
    row_length  = len(table[0])
    r_check_length = row_length - 3

    #P1 Solution
    for i in range(table_length):
        for j,val in enumerate(table[i]):
            if table[i][j] != 'X': continue #we're not on the start of a word
            if i >= 3: #Check  up
                if j >= 3: #Check up left
                    if checkXMAS((i-1,j-1),(i-2,j-2),(i-3,j-3)): p1 += 1
                #Check up
                if checkXMAS((i-1,j),(i-2,j),(i-3,j)): p1 += 1
                if j < r_check_length: #check up right
                    if checkXMAS((i-1,j+1),(i-2,j+2),(i-3,j+3)): p1 += 1
            #Check cur row
            if j >= 3: #Check left
                if checkXMAS((i,j-1),(i,j-2),(i,j-3)): p1 += 1
            if j < r_check_length: #check right
                if checkXMAS((i,j+1),(i,j+2),(i,j+3)): p1 += 1
            #Check down
            if i < t_check_length:
                if j >= 3: #Check down left
                    if checkXMAS((i+1,j-1),(i+2,j-2),(i+3,j-3)): p1 += 1
                #Check down
                if checkXMAS((i+1,j),(i+2,j),(i+3,j)): p1 += 1
                if j < r_check_length: #check down right
                    if checkXMAS((i+1,j+1),(i+2,j+2),(i+3,j+3)): p1 += 1

    t_check_length = table_length - 1
    r_check_length = row_length - 1

    #P2 Solution
    for i in range(1,t_check_length):
        for j in range(1,r_check_length):
            if table[i][j] != 'A': continue #we're not on the start of a word
            if P2Valid(i,j): p2+=1


    print(p1)
    print(p2)
