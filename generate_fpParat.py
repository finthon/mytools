# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     generate_fpParat
   Description :
   Author :       DrZ
   date：          2023/2/5
-------------------------------------------------
   Change Activity:
                   2023/2/5:
-------------------------------------------------
"""
import numpy as np
import itertools


def generate_fpParas(elements,
                     g1_eta,
                     delta_rs,
                     g2_eta,
                     g2_zeta,
                     delta_theta,
                     lambda_=1,
                     rcut=6.0):
    g1_list = []
    for i in elements:
        for j in elements:
            g1_list.append([i, j])
    rs_list = np.arange(1.5, 6.005, delta_rs)
    theta_list = np.arange(0, np.pi+0.005, delta_theta)
    n = len(elements)
    g1_number = len(rs_list) * len(g1_list)
    g2_number = n * len(theta_list) * len(g1_list)
    file = open('fpParas.dat', 'w')
    file.write('# FP type\n')
    file.write('BP\n')
    file.write('# Elements\n')
    file.write(' '.join(elements) + '\n')
    cohesive = '0.0 ' * n + '\n'
    file.write(cohesive)
    file.write('# nG1s nG2s\n')
    file.write('{}  {}\n'.format(g1_number, g2_number))
    file.write('#type  center neighbor   eta       Rs   Rcut\n')
    for ele in g1_list:
        for rs in rs_list:
            file.write('G1      {}       {}      {}     {:.3f}  {}\n'.format(ele[0], ele[1], g1_eta, rs, rcut))
    file.write('#type  center neighbor1 neighbor2  eta    zeta   lambda   thetas  rcut\n')
    for e in elements:
        for ele in g1_list:
            for theta in theta_list:
                file.write(
                    'G2      {}       {}       {}     {}     {}      {}      {:.3f}   {}\n'.format(e, ele[0], ele[1], g2_eta,
                                                                                               g2_zeta, lambda_, theta,
                                                                                               rcut))


generate_fpParas(
    elements=['Mo', 'Ni'],
    g1_eta=100,
    delta_rs=0.08,
    g2_eta=0.001,
    g2_zeta=90,
    delta_theta=0.2,
    lambda_=1,
    rcut=6.0
    )