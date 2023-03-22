# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     color_atoms
   Description :
   Author :       DrZ
   date：          2023/2/7
-------------------------------------------------
   Change Activity:
                   2023/2/7:
-------------------------------------------------
"""
import ase
import numpy as np
import pandas as pd
import aseCalcF as acf
from ase.io import Trajectory


def get_true_e_and_f(data_path):
    true_energy = []
    true_force = []
    data = Trajectory(data_path)
    i = 0
    for ge in data:
        true_energy.append(ge.get_potential_energy())
        true_force.append(ge.get_forces())
        i += 1
        if i % 10 == 0:
            print('Get the real energy and force of the {}th image in the test set.'.format(i))
    return true_energy, true_force


def get_pred_e_and_f(data_path, model):
    pred_energy = []
    pred_force = []
    i = 0
    data = Trajectory(data_path)
    for ge in data:
        ge.set_calculator(model)
        pred_energy.append(ge.get_potential_energy())
        pred_force.append(ge.get_forces())
        i += 1
        if i % 10 == 0:
            print('Predict the energy and force of the {}th image in the test set.'.format(i))
    return pred_energy, pred_force


def get_rmse_e_and_f(pred_energy, pred_force, true_energy, true_force):
    num = len(pred_energy)
    er_e_list = []
    error_energy = np.array(pred_energy) - np.array(true_energy)
    i = 0
    for e_e in error_energy:
        er_e_list.append(e_e / len(true_force[i]))
        i += 1
        if i % 10 == 0:
            print('Calculate the EnergyRMSE of the {}th image.'.format(i))
    rmse_e = np.sqrt(sum((np.array(er_e_list) ** 2)) / num)
    # er_f_list = []
    # error_force = np.array(pred_force) - np.array(true_force)
    # i = 0
    # for e_f in error_force:
    #     er_f_list.append(np.sqrt(sum(sum(e_f ** 2)) / (3 * len(e_f))))
    #     i += 1
    #     if i % 10 == 0:
    #         print('Calculate the ForceRMSE of the {}th image.'.format(i))
    # rmse_f = np.sqrt(sum(np.array(er_f_list) ** 2) / num)
    er_f_list = []
    for n, img in enumerate(true_force):
        delta_f = np.array(img) - np.array(pred_force[n])
        img_f = np.sum(delta_f ** 2) / 3 / len(img)
        er_f_list.append(img_f)
    rmse_f = np.sqrt(np.average(np.array(er_f_list)))
    return rmse_e, rmse_f


def write_e_and_f_to_file(true_energy, pred_energy, true_force, pred_force):
    num = len(true_force)
    true_energy_num = []
    pred_energy_num = []
    pred_force_num = []
    true_force_num = []
    for i in range(num):
        true_energy_num.append(true_energy[i] / len(true_force[i]))
        pred_energy_num.append(pred_energy[i] / len(true_force[i]))
    data_e = pd.DataFrame()
    data_e['true_energy'] = true_energy_num
    data_e['pred_energy'] = pred_energy_num
    data_e.to_excel('energy.xlsx', sheet_name='energy', index=True)

    data = pd.DataFrame()
    for f_ in true_force:
        data_f = pd.DataFrame()
        f_x = []
        f_y = []
        f_z = []
        for i in range(len(f_)):
            f_x.append(f_[i][0])
            f_y.append(f_[i][1])
            f_z.append(f_[i][2])
        data_f['true_force_x'] = f_x
        data_f['true_force_y'] = f_y
        data_f['true_force_z'] = f_z
        data = pd.concat([data, data_f], axis=0)
    data.to_excel('force_true.xlsx', sheet_name='force_t', index=True)

    data = pd.DataFrame()
    for f_ in pred_force:
        data_f = pd.DataFrame()
        f_x = []
        f_y = []
        f_z = []
        for i in range(len(f_)):
            f_x.append(f_[i][0])
            f_y.append(f_[i][1])
            f_z.append(f_[i][2])
        data_f['pred_force_x'] = f_x
        data_f['pred_force_y'] = f_y
        data_f['pred_force_z'] = f_z
        data = pd.concat([data, data_f], axis=0)
    data.to_excel('force_p.xlsx', sheet_name='force_p', index=True)


my_model = acf.aseCalcF()
pa = 'NiMo_train.traj'
print('====================================Start-a-job====================================')
print('1.Get real energy and force.')
true_energy, true_force = get_true_e_and_f(data_path=pa)
print('2.Get the predicted energy and force.')
pred_energy, pred_force = get_pred_e_and_f(data_path=pa, model=my_model)
print('3.Write the real and predicted energy and force into a file and save it as an excel table.')
write_e_and_f_to_file(true_energy, pred_energy, true_force, pred_force)
print('4.Calculate the EnergyRMSE and ForceRMSE of the test set.')
rmse_e, rmse_f = get_rmse_e_and_f(pred_energy=pred_energy, pred_force=pred_force,
                                  true_energy=true_energy, true_force=true_force)

print('**************EnergyRMSE={},ForceRMSE={}**************'.format(rmse_e, rmse_f))
print('====================================D-o-n-e====================================')

