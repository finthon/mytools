from __future__ import division
from ase.io import read, Trajectory
from collections import Counter
import sys
import numpy as np

import math

from ase.neighborlist import NeighborList
from ase.calculators.calculator import Calculator, all_changes
from ase.calculators.calculator import PropertyNotImplementedError


class force_setter(Calculator):
    implemented_properties = ['energy', 'forces']
    default_parameters = {'epsilon': 1.0,
                          'sigma': 1.0,
                          'rc': None}
    nolabel = True

    def __init__(self, energy=None, forces=None,**kwargs):
        Calculator.__init__(self, **kwargs)
        self.energy = energy
        self.forces = forces

    def calculate(self, atoms=None, 
                  properties=['energy'],
                  system_changes=all_changes):
        Calculator.calculate(self, atoms, properties, system_changes)

#        natoms = len(self.atoms)
        
#        positions = self.atoms.positions
#        cell = self.atoms.cell

        self.results['energy'] = self.energy
        self.results['forces'] = self.forces

args=sys.argv
imgs = read(args[1], index=":")
trajs = Trajectory('supercell.traj','w')
Rcut = 6.0
imgIndex = 0
for img in imgs:
  print("img:",imgIndex)
  imgIndex+=1
  unitvector = img.get_cell()
  unitE = img.get_potential_energy()
  unitF = img.get_forces()
  unitCell = img.cell
  latticeparas = unitCell.cellpar(radians=True)
  cross_vect = np.cross(unitCell[0][:], unitCell[1][:])  # a X b
  a_vertical = np.linalg.norm(unitCell[0][:])
  b_vertical = latticeparas[1] * math.sin(latticeparas[5])
  #if  
  c_vertical = np.dot(unitCell[2][:], cross_vect)/np.linalg.norm(cross_vect)
  #b_vertical = np.dot(unitCell[1][:], unitCell[0][:])/np.linalg.norm(unitCell[0][:])
  print(c_vertical, b_vertical)
  na = math.ceil(2.0*Rcut/a_vertical)
  nb = abs(math.ceil(2.0*Rcut/b_vertical))
  nc = math.ceil(2.0*Rcut/c_vertical)
  #print(unitF)
  #print(img.get_positions())
  #print('   ')
  print(na, nb, nc)
  supercell = img.copy()
  forces = unitF
  energy = unitE
  for i in range(na):
    temp = img.copy()
    temp.set_positions(img.get_positions()+ i*unitvector[0][:])
    supercell.extend(temp)
    energy += unitE
    forces =np.concatenate((forces,unitF))
    #[len(a), len(b), len(c), angle(b,c), angle(a,c), angle(a,b)]
    #print(img.cell.cellpar())
    #print(img.cell.cellpar())
  supercell.set_cell(unitvector*np.array([[na],[1],[1]]))
  unitE=energy
  unitF=forces
  unitvector = supercell.get_cell()
  supercell_1 = supercell.copy()
  for i in range(nb):
    temp = supercell.copy()
    temp.set_positions(supercell.get_positions()+ i*unitvector[1][:])
    supercell_1.extend(temp)
    energy += unitE
    forces =np.concatenate((forces,unitF))
  supercell_1.set_cell(unitvector*np.array([[1],[nb],[1]]))
  unitE=energy
  unitF=forces
  unitvector = supercell_1.get_cell()
  supercell_2 = supercell_1.copy()
  for i in range(nc):
    temp = supercell_1.copy()
    temp.set_positions(supercell_1.get_positions()+ i*unitvector[2][:])
    supercell_2.extend(temp)
    energy += unitE
    forces =np.concatenate((forces,unitF))
  supercell_2.set_cell(unitvector*np.array([[1],[1],[nc]]))
  calc = force_setter(energy=energy, forces=forces)
  supercell_2.set_calculator(calc)
  supercell_2.get_potential_energy()
  supercell_2.get_forces()
  #print(img.get_positions())
  trajs.write(supercell_2)
