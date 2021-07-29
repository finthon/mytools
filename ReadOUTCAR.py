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
import re
import numpy as np
from collections import OrderedDict


class ReadOUTCAR:
    """
    read OUTCAR file
    """
    def __init__(self, filename):
        self.n = 0  # structure_num
        self.filename = filename
        self.end_regex = '^\s*-.*-\s*$'
        self.position_force_dict = OrderedDict()
        self.force_regex = re.compile(r"^\s*POSITION\s+TOTAL-FORCE\s*\(eV\/Angst\)\s*$")

    def get_all_positions_forces(self):
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
                self.position_force_dict[self.n] = {}
                self.position_force_dict[self.n]['positions'] = []
                self.position_force_dict[self.n]['forces'] = []
                f.readline()

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
                        self.position_force_dict[self.n]['positions'].append([xx, yy, zz])
                        self.position_force_dict[self.n]['forces'].append([fx, fy, fz])
                    else:
                        break

                self.position_force_dict[self.n]['positions'] = np.array(self.position_force_dict[self.n]['positions'])
                self.position_force_dict[self.n]['forces'] = np.array(self.position_force_dict[self.n]['forces'])

        return self.position_force_dict

    def get_positions(self, step=-1):
        """
        get posiitons of step, default: the position of last structure
        return positions array
        """

        pfd = self.get_all_positions_forces()
        kl = list(pfd.keys())
        if step > 0:
            nn = kl[step-1]
            return self.get_all_positions_forces()[nn]['positions']
        if step < 0:
            nn = kl[step]
            return self.get_all_positions_forces()[nn]['positions']
        else:
            raise Exception('Wrong index with step=0')

    def get_forces(self, step=-1):
        """
        get forces of step, default: the force of last structure
        return forces array
        """
        kl = list(self.get_all_positions_forces().keys())
        if step > 0:
            nn = kl[step-1]
            return self.get_all_positions_forces()[nn]['forces']
        if step < 0:
            nn = kl[step]
            return self.get_all_positions_forces()[nn]['forces']
        else:
            raise Exception('Wrong index with step=0')


if __name__ == '__main__':
    filename = 'OUTCAR'
    ro = ReadOUTCAR(filename)
    print(ro.get_all_positions_forces()[12])      # the 12th step
    print(ro.get_positions(step=12))
    print(ro.get_forces(step=12))


