# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     plot_loss_change
   Description :
   Author :       DrZ
   date：          2021/2/4
-------------------------------------------------
   Change Activity:
                   2021/2/4:
-------------------------------------------------
"""
import re
import numpy as np
import matplotlib.pyplot as plt

# search epoch data
reg = re.compile('\s+\d+\s+\d+.\d+\s+\d+.\d+\s+\d+.\d+\n')

loss_list = []
energy_list = []
force_list = []
with open('pyamff.log', 'r') as f:
    for line in f:
        result = reg.search(line)
        if result is not None:
            result = result.group().strip()
            result = re.split('\s+', result)
            loss = result[1]
            energy = result[2]
            force = result[3]
            loss_list.append(float(loss))
            energy_list.append(float(energy))
            force_list.append(float(force))

x = [i for i in range(1, len(loss_list)+1)]
# energy
plt.figure()
plt.plot(x, energy_list)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Epoch', size=14)
plt.ylabel('Energy RMSE', size=14)
plt.annotate(s=str(np.round(energy_list[-1], 2)), xy=(x[-1], energy_list[-1]),
             xytext=(x[-1]*0.9, energy_list[-1]+(max(energy_list)-min(energy_list))*0.1),
             arrowprops=dict(arrowstyle='->'), fontsize=12)
plt.tight_layout()
plt.savefig('energy_rmse.png', dpi=300)
#plt.show()

# loss
plt.figure()
plt.plot(x, loss_list)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Epoch', size=14)
plt.ylabel('LossValue', size=14)
plt.annotate(s=str(np.round(loss_list[-1], 2)), xy=(x[-1], loss_list[-1]),
             xytext=(x[-1]*0.8, loss_list[-1]+(max(loss_list)-min(loss_list))*0.1),
             arrowprops=dict(arrowstyle='->'), fontsize=12)
plt.tight_layout()
plt.savefig('loss_rmse.png', dpi=300)
#plt.show()

# force
plt.figure()
plt.plot(x, force_list)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Epoch', size=14)
plt.ylabel('Force RMSE', size=14)
plt.annotate(s=str(np.round(force_list[-1], 2)), xy=(x[-1], force_list[-1]),
             xytext=(x[-1]*0.9, force_list[-1]+(max(force_list)-min(force_list))*0.1),
             arrowprops=dict(arrowstyle='->'), fontsize=12)
plt.tight_layout()
plt.savefig('force_rmse.png', dpi=300)
#plt.show()
