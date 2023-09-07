# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       DrZ
   date：          2023/9/7
-------------------------------------------------
   Change Activity:
                   2023/9/7:
-------------------------------------------------
"""
import sys
import numpy as np
from vaspy.atomco import PosCar


"""
check IS and FS atom index and revised CONTCAR(FS) consistent with IS.
Usage: check_neb_dist CONTCAR(IS) CONTCAR(FS) move_atom_list
e.g. if move_atoms index in ase.gui is 0 3 4;   check_neb_dist CONTCAR CONTCAR 0 3 4 
tips: CONTCAR need absolute path
"""

def expand_coord(point, aa, bb):
    tran1 = point + aa
    tran2 = point + aa + bb
    tran3 = point + aa - bb
    tran4 = point - aa
    tran5 = point - aa + bb
    tran6 = point - aa - bb
    tran7 = point + bb
    tran8 = point - bb
    point_sum = [point, tran1, tran2, tran3, tran4, tran5, tran6, tran7, tran8]
    return point_sum


def get_index(CON_IS, CON_FS, move_list):
    """
    :param CON_IS: CONTCAR_IS
    :param CON_FS: CONTCAR_FS
    :param move_list: NEB move atoms
    :return: an index list with the correct sort
    """
    pos_is = PosCar(CON_IS)
    pos_fs = PosCar(CON_FS)
    pos_is_data = pos_is.data
    pos_fs_data = pos_fs.data
    aa = pos_is.bases[0]
    bb = pos_is.bases[1]
    # convert to cartesian
    cart_is = pos_is.dir2cart(pos_is.bases, pos_is_data)
    cart_fs = pos_fs.dir2cart(pos_fs.bases, pos_fs_data)
    # convert to n*3 array, due to only one atom with 3*1 shape.
    if cart_is.shape == (3,):
        cart_is = cart_is.reshape(-1, 3)
    if cart_fs.shape == (3,):
        cart_fs = cart_fs.reshape(-1, 3)

    # expand all FS coord
    all_FS_coord = []
    for ccc in cart_fs:
        all_FS_coord.extend(expand_coord(ccc, aa, bb))

    index_list = []
    # screen every coord in IS
    for num, coord in enumerate(cart_is):
        #print('atom: {} start'.format(num))
        if num in move_list:
            index_list.append(num)
        else:
            all_dist = []
            coord_sum = expand_coord(coord, aa, bb)
            for point_one in coord_sum:
                for point_two in all_FS_coord:
                    dist = np.linalg.norm(point_one - point_two)
                    all_dist.append(dist)
            ind = np.argsort(all_dist)[0] % 1323 # 取余
            ind = ind // 9  # 取整
            index_list.append(ind)
    return index_list


def generate_CONT(CON_FS, index):
    # generate New CONTCAR
    file_fs = open(CON_FS, 'r')
    data = file_fs.readlines()
    file_fs.close()
    # header
    qian_zhui = data[:9]
    new_data = []
    for inx in index:
        new_data.append(data[9:][inx])
    # rewrite
    f = open('CONTCAR_rec', 'w')
    f.writelines(qian_zhui)
    f.writelines(new_data)
    f.close()


if __name__ == '__main__':
    file_name = sys.argv[0]
    contcar_is = sys.argv[1]
    contcar_fs = sys.argv[2]
    ts_atoms = sys.argv[3:]
    ts_atoms = [int(i) for i in ts_atoms]
    ind = get_index(contcar_is, contcar_fs, ts_atoms)
    generate_CONT(contcar_fs, ind)
