# -*- coding: utf-8 -*-
"""
created by Dr.Z  2022/2/12
usage: zcd jobid
e.g. zcd 312242
"""
import os
import re
import sys
import subprocess

jobid = sys.argv[1]
subprocess.call('bjobs -l {} > temp'.format(jobid), shell=True)
f = open('temp', 'r')
p = ''
for cc in f:
    p = p + cc.strip()
f.close()
os.remove('temp')
x = re.search('Execution CWD <.+.+>', p)
if x is not None:
    xx = re.search('<.+\n*.+>', x.group())
    yy = re.split('\s+', xx.group())
    if len(yy) == 1:
        path = yy[0].strip('<>')
    else:
        path = ''
        for st in yy:
            path = path + st
        path = path.strip('<>')
else:
    try:
        zz = re.search(r'CWD <.HOME/.+.+>,.*Output', p)
        if zz is None:
            zz = re.search(r'CWD <.HOME/.+.+>', p)
        zz = re.search('<.+\n*.+>', zz.group())
    except:
        zz = re.search(r'CWD </data/.+.+>,.*Output', p)
        if zz is None:
            zz = re.search(r'CWD </data/.+.+>', p)
        zz = re.search('<.+\n*.+>', zz.group())
    zz = re.split('\s+', zz.group())
    path = zz[0].strip('<>')
print(path)

