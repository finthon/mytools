# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     check_neb_dist
   Description :
   Author :       DrZ
   date：          2023/6/5
-------------------------------------------------
   Change Activity:
                   2023/6/5:
-------------------------------------------------
"""
import re
import sys
import numpy as np

"""
check IS and FS atom index and revised CONTCAR(FS) consistent with IS.
Usage: check_neb_dist CONTCAR(IS) CONTCAR(FS) move_atom_list
e.g. if move_atoms index in ase.gui is 0 3 4;   check_neb_dist CONTCAR CONTCAR 0 3 4 
tips: CONTCAR need absolute path
"""


def read_contcar(contcar):
    file_is = open(contcar, 'r')
    data = file_is.readlines()
    file_is.close()
    # header
    qian_zhui = data[:9]
    # atom numbers
    num = data[6]
    a = re.split('\s+', num.strip())
    num = sum([int(i) for i in a])
    # coord array
    coord = data[9:9 + num]
    coord_list = []
    for i in coord:
        a = re.split('\s+', i.strip())
        coord_list.append([float(a[0]), float(a[1]), float(a[2])])
    coord_array = np.array(coord_list)
    return coord_array, num, qian_zhui


def compare_data(is_file, fs_file, ts_atoms, threshold_value=0.2):
    IS, num, qian_zhui = read_contcar(is_file)
    FS, num, qian_zhui = read_contcar(fs_file)
    dist_array = np.zeros((num, 1))
    for nu in range(num):
        dist_nu = np.linalg.norm(IS[nu] - FS[nu])
        dist_array[nu] = dist_nu

    condition = np.sum(dist_array > threshold_value)
    if condition == len(ts_atoms):
        print('IS and FS consistent')
    else:
        print('Warning: Inconsistent, revising CONTCAR_FS to CONTCAR_re...')
        f = open('CONTCAR_re', 'w')
        f.writelines(qian_zhui)
        file_fs = open(fs_file, 'r')
        data = file_fs.readlines()
        coord = data[9:9 + num]
        index_list = []
        for n, i in enumerate(IS):
            if n in ts_atoms:
                f.write(coord[n])
                index_list.append(n)
            else:
                all_dist = [np.linalg.norm(i - j) for j in FS]
                ind = np.argmin(all_dist)
                nn = 1
                while True:
                    if ind in index_list:
                        ind = np.argsort(np.array(all_dist))[nn]
                        nn += 1
                    else:
                        break
                f.write(coord[ind])
                index_list.append(ind)
        f.close()


if __name__ == '__main__':
    file_name = sys.argv[0]
    contcar_is = sys.argv[1]
    contcar_fs = sys.argv[2]
    ts_atoms = sys.argv[3:]
    compare_data(contcar_is,
                 contcar_fs,
                 ts_atoms=ts_atoms,
                 threshold_value=0.2)

