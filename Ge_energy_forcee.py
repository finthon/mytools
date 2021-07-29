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
    refe_atom = (img.get_potential_energy(apply_constraint=False)
                  - np.dot(np.array(nelems), np.array(res)))/len(img)
    refe = img.get_potential_energy(apply_constraint=False)
    reffs = img.get_forces()
    img.set_calculator(calc)
    prede_atom = img.get_potential_energy()
    prede = img.get_potential_energy()*len(img)+np.dot(np.array(nelems), np.array(res))
    eout.write("{:8}  {:12.9f} {:12.9f} {:12.9f} {:12.9f}\n".format(i+1, refe, prede, refe_atom, prede_atom))
    forces = len(img) * img.get_forces()
    #forces = img.get_forces()
    for j in range(len(img)):
      fout.write("{:8}_x  {:12.9f} {:12.9f}\n".format(i+1, reffs[j][0], forces[j][0]))
      fout.write("{:8}_y  {:12.9f} {:12.9f}\n".format(i+1, reffs[j][1], forces[j][1]))
      fout.write("{:8}_z  {:12.9f} {:12.9f}\n".format(i+1, reffs[j][2], forces[j][2]))
    fout.flush()
    eout.flush()
    if img.get_potential_energy() < 0:
      print(i+1, file=f_err)
    i += 1
    print('{} done.'.format(i))

f_err.close()
fout.close()
eout.close()
