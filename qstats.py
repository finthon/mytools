# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     qstats
   Description :
   Author :       DrZ
   date：          2023/8/30
-------------------------------------------------
   Change Activity:
                   2023/8/30:
-------------------------------------------------
"""
import os
import re
import subprocess

jobid_list = []
user_list = []
stat_list = []
jobname_list = []
subtime_list = []
runtime_list = []
walltime_list = []
path_list = []

subprocess.call('qstat > temp_jobs', shell=True)
f = open('temp_jobs', 'r')
os.remove('temp_jobs')

finthon = False
for idx, line in enumerate(f):
    if (idx == 0) and (re.split('\s+', line)[0] != 'Job'):
        print('There no job submitted!')
        finthon = True
        break
    elif idx == 0 or idx == 1:
        continue
    else:
        jobid_list.append(re.split('\s+', line.strip())[0].split('.')[0])
f.close()

if finthon is False:
    for n, i in enumerate(jobid_list):
        subprocess.call('qstat -f {} > temp{}'.format(i, n), shell=True)
        f = open('temp{}'.format(n), 'r')
        p = ''
        for cc in f:
            p = p + cc.strip()
        x = re.search('Output_Path.*Priority', p)
        xx = re.search('/.*/', x.group())
        path_list.append(xx.group())
        f.close()
        f = open('temp{}'.format(n), 'r')
        os.remove('temp{}'.format(n))
        for no, line in enumerate(f):
            line_list = re.split('\s+', line.strip())
            if line_list[0] == 'Job_Name':
                jobname_list.append(line_list[2])
            if line_list[0] == 'Job_Owner':
                user_list.append(line_list[2].split('@')[0])
            if no == 8 and line_list[0] == 'resources_used.walltime':
                walltime_list.append(line_list[2])
            if line_list[0] == 'job_state':
                stat_list.append(line_list[2])
            if line_list[0] == 'qtime':
                subtime_list.append(' '.join(line_list[3:6]))
            # if line_list[0] == 'Error_Path':
            #     rpath = re.search('/.*/', line_list[2])
            #     path_list.append(rpath.group())
            if line_list[0] == 'stime':
                runtime_list.append(' '.join(line_list[3:6]))
        if len(walltime_list) < len(jobname_list):
            walltime_list.append('--:--:--')
        if len(runtime_list) < len(jobname_list):
            runtime_list.append('--- -- --:--:--')
        f.close()
    print("\033[1;31m{:<4}\033[0m\033[1;33m{:<7}\033[0m\033[1;31m{:<10}\033[0m\033[1;37m{:<3}\033[0m\033[1;34m{:<20}\033[0m\033[1;35m{:<18}\033[0m\033[1;34m{:<18}\033[0m\033[1;32m{:<11}\033[0m\033[1;36m{:<10}\033[0m".format("No", "JOBID", "USER", "S", "JOB_NAME",
                                                                       "SUB_TIME", "RUN_TIME", "WALL_TIME", "PATH"))
    for i in range(len(jobid_list)):
        print("\033[1;31m{:<4}\033[0m\033[1;33m{:<7}\033[0m\033[1;31m{:<10}\033[0m\033[1;37m{:<3}\033[0m\033[1;34m{:<20}\033[0m\033[1;35m{:<18}\033[0m\033[1;34m{:<18}\033[0m\033[1;32m{:<11}\033[0m\033[1;36m{:<10}\033[0m".format(i+1, jobid_list[i], user_list[i],
                                                    stat_list[i], jobname_list[i],
                                                    subtime_list[i], runtime_list[i],
                                                    walltime_list[i], path_list[i]))
