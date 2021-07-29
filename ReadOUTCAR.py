# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_vasp_read_outcar
   Description :
   Author :       DrZ
   date：          2021/7/29
-------------------------------------------------
   Change Activity:
                   2021/7/29:
-------------------------------------------------
"""
import os
import re
import sys
import numpy as np
from collections import OrderedDict


class ReadOUTCAR:
    """
    read OUTCAR file
    """
    def __init__(self, filename):
        self.cell_list = []
        self.n = 0  # structure_num
        self.filename = filename
        self.end_regex = r'^\s*-.*-\s*$'
        self.energy_regex = r'^\s*energy  without entropy=.*energy\(sigma->0\).*\s*$'
        self.position_force_energy_dict = OrderedDict()
        self.force_regex = re.compile(r"^\s*POSITION\s+TOTAL-FORCE\s*\(eV\/Angst\)\s*$")
        self.cell_regex = r'^\s*direct lattice vectors\s*reciprocal lattice vectors\s*$'

    def get_all_positions_forces_energies(self):
        """
        get all positions and forces of all ion-step structures, dict type
        {1: {'positions': array, 'forces': array},
         2: {'positions': array, 'forces': array},
         3: {'positions': array, 'forces': array},
         4: {'positions': array, 'forces': array},
         ...}
        """
        f = open(self.filename, 'r')

        for i in f:
            if self.force_regex.match(i):
                self.n += 1
                self.position_force_energy_dict[self.n] = {}
                self.position_force_energy_dict[self.n]['positions'] = []
                self.position_force_energy_dict[self.n]['forces'] = []
                self.position_force_energy_dict[self.n]['energies'] = []

                f.readline()
                # get positions and forces
                while True:
                    aa = f.readline().strip()
                    _x = re.search(self.end_regex, aa)
                    if not _x:
                        fin = re.split('\s+', aa)
                        xx = float(fin[0])
                        yy = float(fin[1])
                        zz = float(fin[2])
                        fx = float(fin[3])
                        fy = float(fin[4])
                        fz = float(fin[5])
                        self.position_force_energy_dict[self.n]['positions'].append([xx, yy, zz])
                        self.position_force_energy_dict[self.n]['forces'].append([fx, fy, fz])
                    else:
                        break
                # get energies
                n = 0
                while n >= 2:
                    aa = f.readline()
                    _x = re.search(self.end_regex, aa)
                    if _x:
                        n += 1
                while True:
                    aa = f.readline()
                    _x = re.search(self.energy_regex, aa)
                    if _x:
                        en_str = _x.group().strip()
                        fin = re.split('\s+', en_str)
                        self.position_force_energy_dict[self.n]['energies'].append(float(fin[-1]))
                        break

                self.position_force_energy_dict[self.n]['positions'] = np.array(self.position_force_energy_dict[self.n]['positions'])
                self.position_force_energy_dict[self.n]['forces'] = np.array(self.position_force_energy_dict[self.n]['forces'])

        f.close()
        return self.position_force_energy_dict

    def get_cells(self):
        """
        get cells matrix from OUTCAR, array type
        """
        f = open(self.filename, 'r')
        for i in f:
            bb = re.search(self.cell_regex, i)
            if bb:
                for jj in range(3):
                    _x1 = f.readline().strip()
                    fin = re.split('\s+', _x1)
                    self.cell_list.append([float(fin[0]), float(fin[1]), float(fin[2])])
                break

        cell_array = np.array(self.cell_list)
        f.close()
        return cell_array

    def get_potential_energies(self, step=-1):
        """
        get potential energies (sigma->0) of step, default: the energy of last structure
        return a float
        """
        kl = list(self.get_all_positions_forces_energies())
        if step > 0:
            nn = kl[step - 1]
            return self.get_all_positions_forces_energies()[nn]['energies'][0]
        if step < 0:
            nn = kl[step]
            return self.get_all_positions_forces_energies()[nn]['energies'][0]
        else:
            raise Exception('Wrong index with step=0')

    def get_positions(self, step=-1):
        """
        get posiitons of step, default: the position of last structure
        return positions array
        """
        kl = list(self.get_all_positions_forces_energies())
        if step > 0:
            nn = kl[step-1]
            return self.get_all_positions_forces_energies()[nn]['positions']
        if step < 0:
            nn = kl[step]
            return self.get_all_positions_forces_energies()[nn]['positions']
        else:
            raise Exception('Wrong index with step=0')

    def get_forces(self, step=-1):
        """
        get forces of step, default: the force of last structure
        return forces array
        """
        kl = list(self.get_all_positions_forces_energies().keys())
        if step > 0:
            nn = kl[step-1]
            return self.get_all_positions_forces_energies()[nn]['forces']
        if step < 0:
            nn = kl[step]
            return self.get_all_positions_forces_energies()[nn]['forces']
        else:
            raise Exception('Wrong index with step=0')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]  # input "python ReadOUTCAR.py OUTCAR" on Terminal
    else:
        filename = 'OUTCAR'     # or give outcar path by hand here
    ro = ReadOUTCAR(filename)
    print(ro.get_positions(step=12))
    print(ro.get_forces(step=-1))
    print(ro.get_cells(step=-1))
    print(ro.get_potential_energies(step=-1))






