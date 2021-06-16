# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     generate_xsd
   Description :
   Author :       DrZ
   date：          2021/3/11
-------------------------------------------------
   Change Activity:
                   2021/3/11:
-------------------------------------------------
"""
import re
import sys
from ase.io import xsd
from ase.io.vasp import read_vasp


def generate_xsd(file='CONTCAR'):
    """
    default: reading CONTCAR file
    Usage: python generate_xsd.py CONTCAR
        or python generate_xsd.py POSCAR
        or python generate_xsd.py
        or python generate_xsd.py POSCAR_2
        or python generate_xsd.py CONTCAR_x
    filename just includes CONTCAR or POSCAR, that is OK!
    """
    if re.search('CONTCAR|POSCAR', file) is not None:
        pos = read_vasp(file)
        pos.set_pbc([True, True, True])
        xsd.write_xsd('{}.xsd'.format(file), pos)
    else:
        raise Exception("Please add a CONCAR or POSCAR!")


if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) == 2:
        file = sys.argv[-1]
        generate_xsd(file)
    elif len(argvs) == 1:
        generate_xsd()
    else:
        raise Exception("Wrong Usage for generate_xsd.py, Please check the input!")
