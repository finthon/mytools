# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sumdos_zc
   Description :
   Author :       DrZ
   date：          2019/11/23
-------------------------------------------------
   Change Activity:
                   2019/11/23:
-------------------------------------------------
"""
import pandas as pd
import sys
import os

file_name = sys.argv[0]
DOS_range = sys.argv[1:]

pwd = os.getcwd()

t_tp, t_tn, t_sp, t_sn, t_pp, t_pn, t_dp, t_dn, t_fp, t_fn, t_dz2p, t_dz2n, t_pdp, t_pdn = [0] * 14

for i in range(int(DOS_range[0]), int(DOS_range[1]) + 1):
    df = pd.read_csv(os.path.join(pwd, 'DOS{}'.format(str(i))), header=None, sep='\s+')
    df_sp = df[1]
    df_sn = df[2]
    df_pp = df[3] + df[5] + df[7]
    df_pn = df[4] + df[6] + df[8]
    df_dp = df[9] + df[11] + df[13] + df[15] + df[17]
    df_dz2p = df[13]
    df_dz2n = df[14]
    df_dn = df[10] + df[12] + df[14] + df[16] + df[18]
    df_fp = df[19] + df[21] + df[23] + df[25] + df[27] + df[29] + df[31]
    df_fn = df[20] + df[22] + df[24] + df[26] + df[28] + df[30] + df[32]
    df_totalp = df_sp + df_pp + df_dp + df_fp
    df_totaln = df_sn + df_pn + df_dn + df_fn
    df_pdp = df_pp + df_dp
    df_pdn = df_pn + df_dn
    t_tp += df_totalp
    t_tn += df_totaln
    t_sp += df_sp
    t_sn += df_sn
    t_pp += df_pp
    t_pn += df_pn
    t_dp += df_dp
    t_dn += df_dn
    t_fp += df_fp
    t_fn += df_fn
    t_dz2p += df_dz2p
    t_dz2n += df_dz2n
    t_pdp += df_pdp
    t_pdn += df_pdn

data = pd.DataFrame()
data['Energy'] = df[0]
data['total+'] = t_tp
data['total-'] = t_tn
data['s+'] = t_sp
data['s-'] = t_sn
data['p+'] = t_pp
data['p-'] = t_pn
data['d+'] = t_dp
data['d-'] = t_dn
data['f+'] = t_fp
data['f-'] = t_fn
data['dz2+'] = t_dz2p
data['dz2-'] = t_dz2n
data['d_total'] = t_dp - t_dn
data['spd'] = t_tp - t_tn
data['dz2'] = t_dz2p - t_dz2n
data['pd'] = t_pdp - t_pdn

data.to_excel('DOS.SUM.{}.to.{}.xlsx'.format(DOS_range[0], DOS_range[1]), index=False)

