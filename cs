#!/bin/env python
import sh
import re
from collections import defaultdict

bosses = ['hfwang', 'xmcao', 'xueqing']
gong_group = ['xueqing', 'tnie', 'zqwang', 'yfang', 'lchen','sybao','fli', 'dwang']
cao_group = ['xmcao', 'wdhu', 'pwang', 'yliu', 'hjzhou', 'yhjin', 'bks', 'lcheng', 'xtsun', 'hhliu', 'cfei', 'kqzhang']
wang_group = ['hfwang', 'hyyuan', 'jwzhang', 'czhou', 'mzhou', 'jfchen', 'cgdong']

boss_group = defaultdict(dict)
results = sh.showq()
runnings = results.split("\n\n")[1]
cpus = runnings.split("\n")

for job in cpus:
    infos = re.split('\s+', job)
    user = infos[1]
    cpu = int(infos[3])
    if user in gong_group:
        if user not in boss_group['xueqing']:
	        boss_group['xueqing'][user] = 0
        boss_group['xueqing'][user] += cpu

    if user in wang_group:
        if user not in boss_group['hfwang']:
	        boss_group['hfwang'][user] = 0
        boss_group['hfwang'][user] += cpu

    if user in cao_group:
        if user not in boss_group['xmcao']:
	        boss_group['xmcao'][user] = 0
        boss_group['xmcao'][user] += cpu

print("{:^16}{:^16}{:^16}{:^16}".format("BOSS", "USER", "CPU/USER", "CPU/GROUP"))

for b in bosses:
    group_cpu = sum(boss_group[b].values())
    for u in boss_group[b].keys():
	    print("{:^16}{:^16}{:^16}{:^16}".format(b, u, boss_group[b][u], group_cpu))
