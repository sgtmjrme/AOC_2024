#!/usr/bin/env python3

import argparse

def add(v1,v2) -> int:
    return v1+v2

def mul(v1,v2) -> int:
    return v1*v2

def pip(v1,v2) -> int:
    return int(f'{v1}{v2}')

def parseLine(line: str) -> 'tuple[int,list[int]]':
    splits = line.strip().split(':')
    return (int(splits[0]),[int(x) for x in splits[1].split()])

def checker(valid_ops,line):
    valid_op_length = len(valid_ops)
    target, nums = parseLine(line)
    numOps = len(nums)-1
    for num in range(pow(valid_op_length,numOps)):
        tmpTarget = nums[0]
        op_str = []
        for i in range(numOps):
            op = valid_ops[int(num/pow(valid_op_length,i))%valid_op_length]
            op_str.append(op.__name__)
            tmpTarget = op(tmpTarget,nums[i+1])
            if tmpTarget > target: break
        else:  #You MUST make it to the end to be valid
            if tmpTarget == target:
                return target
    return 0

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                    help="File")
    args = parser.parse_args()

    p1 = 0
    p2 = 0
    with open(args.filename,'r') as f:
        for line in f:
            p1 += checker([mul,add],line)
            p2 += checker([mul,add,pip],line)
                    
    print(p1)
    print(p2)
