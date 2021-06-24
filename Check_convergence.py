import os
import re
import numpy as np


f = open('check', 'w')

for n in range(2475):
    i = 1
    os.chdir('./{}'.format(n))
    OSZ = r'./OSZICAR'
    CHE = open(OSZ, 'r')
    lines = CHE.readlines()
    last_line = lines[-2]
    #lists = []
    lists1 = re.split('\s+', last_line)[1]
    #lists.append(lists1.strip())
    #print('{}'.format(n))
    if int(lists1) < 500:
        j = i+0
        #print(j)
        #print('file:{}  n:{}  step:{}'.format(n, j, lists1), file=f)
    else:
        j = i-1
        #print(j)
        print('file:{}  n:{}  step:{}'.format(n, j, lists1), file=f)
    #print(lists1)
    #f = open('../check', 'w')
    #f.write{'{}'.format(n), j, lists1}
    #f = close{}
    os.chdir('../')
    print('{} done.'.format(n))
    #input()

f.close()
