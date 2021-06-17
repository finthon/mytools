#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
----------------------------------------
   Time    : 2021/6/16 11:52
   Author  : czhou
   File    : Ge_energy_forcee.py
----------------------------------------
"""
import sys
import numpy as np
from ase.io import read, Trajectory
from pyamff.pyamffCalcF import pyamffCalcF
from collections import OrderedDict, Counter


args = sys.argv  # train.traj
images = read(args[1], index=":")

calc  = pyamffCalcF()
f_err = open('err.dat', 'w')
fout = open('f.dat','w')
eout = open('e.dat','w')
i=0
#saveFF(calc.model, calc.preprocessParas, filename="mlff.pyamff")

#refEs={'Ge':-4.285611335778503}
refEs={'Ge':-4.4899}
for img in images:
    nsymbols = Counter(list(img.symbols))
    nelems = []
    res = []
    for key in refEs:
      if key not in nsymbols:
        continue
      nelems.append(nsymbols[key])
      res.append(refEs[key])
    refe = (img.get_potential_energy(apply_constraint=False)
                  - np.dot(np.array(nelems), np.array(res)))/len(img)
    reffs = img.get_forces()
    img.set_calculator(calc)
    eout.write("{:12.9f} {:12.9f}\n".format(refe, img.get_potential_energy()))
    forces = len(img) * img.get_forces()
    for j in range(len(img)):
      fout.write("{:12.9f} {:12.9f}\n".format(reffs[j][0], forces[j][0]))
      fout.write("{:12.9f} {:12.9f}\n".format(reffs[j][1], forces[j][1]))
      fout.write("{:12.9f} {:12.9f}\n".format(reffs[j][2], forces[j][2]))
    fout.flush()
    eout.flush()
    if img.get_potential_energy() < 0:
      print(i, file=f_err)
    i += 1
    print('{} done.'.format(i))

f_err.close()
fout.close()
eout.close()
