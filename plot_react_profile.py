# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     plot_react_profile
   Description :
   Author :       DrZ
   date：          2021/3/25
-------------------------------------------------
   Change Activity:
                   2021/3/25:
-------------------------------------------------
"""
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


path = os.getcwd()
argvs = sys.argv
# accumulative_freeEnergy.dat file path, put each file behind the script
file_paths = argvs[1:]
plt.figure()

for file in file_paths:
    legend = re.split(r'/', file)[-2]
    with open(file, 'r') as f:
        f = f.readlines()
        # read the last row
        rs = float(re.split('\s+', f[-1].strip())[1])
        ts = float(re.split('\s+', f[-1].strip())[2])
        fs = float(re.split('\s+', f[-1].strip())[3])

        # point1 and point3 is rs and fs, point2 is ts
        x = np.array([0.5, 1, 2, 3, 3.5])
        y = np.array([rs, rs, ts, fs, fs])
        xnew = np.linspace(1, 3, 100)
        func = interpolate.interp1d(x, y, kind='cubic')
        ynew = func(xnew)

        xnew = np.insert(xnew, 0, 0.5)
        xnew = np.append(xnew, 3.5)
        ynew = np.insert(ynew, 0, rs)
        ynew = np.append(ynew, fs)
        plt.plot(xnew, ynew, label=legend)

plt.ylabel('$\Delta$G (eV)')
plt.xlabel('Coordinates')
plt.xticks([])
plt.legend(loc='best', shadow=False, frameon=False)
plt.tight_layout()
plt.savefig('energy.png', dpi=300)
# plt.show()
