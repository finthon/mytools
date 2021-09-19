# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_N_xyz
   Description :
   Author :       DrZ
   date：          2021/8/11
-------------------------------------------------
   Change Activity:
                   2021/8/11:
-------------------------------------------------
"""
import sys


def getNxyz(infile='3w-pos-1.xyz', step=1):
    f = open(infile, 'r')
    f1 = open('{}.xyz'.format(step), 'w')
    line = f.readline()
    a = 1
    while line:
        # read ncow
        if a == step:
            f1.write(line)
        ncow = int(line.strip())
        # read i line
        i_row = f.readline()
        if a == step:
            f1.write(i_row)
        # read structure line
        if a == step:
            for natom in range(ncow):
                f1.write(f.readline())
            break
        else:
            for natom in range(ncow):
                f.readline()

        a += 1
        line = f.readline()


if len(sys.argv) > 1:
    infile = sys.argv[1]  # python get_N_xyz.py amine_2.4_50.xyz 1
    step = int(sys.argv[2])
else:
    infile = 'amine_2.4_50.xyz'
    step = 3     # or give number of step there

getNxyz(infile, step=step)
