import configparser
from ase.io import read, Trajectory
import os
import shutil


class calc_constructor:
    def __init__(self, calc_type, calc_paras):
        self.calc_type = calc_type
        self.calc_paras = calc_paras

    def get_calculator(self):
        calc_paras = self.calc_paras
        if self.calc_type == 'vasp':
            from ase.calculators.vasp import Vasp
            calc = Vasp(
                xc=calc_paras.get('calculator', 'xc'),  # for MD, coarse prec
                prec=calc_paras.get('calculator', 'prec'),
                istart=calc_paras.getint('calculator', 'istart'),
                ispin=calc_paras.getint('calculator', 'ispin'),
                encut=calc_paras.getfloat('calculator', 'encut'),
                ismear=calc_paras.getint('calculator', 'ismear'),
                sigma=calc_paras.getfloat('calculator', 'sigma'),
                nelm=calc_paras.getint('calculator', 'nelm'),
                nelmin=calc_paras.getint('calculator', 'nelmin'),
                algo=calc_paras.get('calculator', 'algo'),
                lwave=calc_paras.getboolean('calculator', 'lwave'),
                lcharg=calc_paras.getboolean('calculator', 'lcharg'),
                lreal=calc_paras.get('calculator', 'lreal'),
                ediffg=calc_paras.getfloat('calculator', 'ediffg'),
                kspacing=calc_paras.getfloat('calculator', 'kspacing'),
                npar=calc_paras.getint('calculator', 'npar'))
        return calc


def vasp2traj():

    traj_saver = Trajectory('vasp_raw.traj', 'w')
    file_list = []

    for i in range(999):
        file_name = '{}.vasp'.format(i)
        if os.path.exists(file_name):
            file_list.append(file_name)

    for name in file_list:
        traj_saver.write(read(name))
        print('[INFO] save {} complete'.format(name))

    return


def move_file(srcfile, dstpath):

    try:
        if not os.path.exists(dstpath):
            os.mkdir(dstpath)
        shutil.move(srcfile, dstpath)
        print("move %s -> %s" % (srcfile, dstpath))

    except Exception as e:
        print(e)
        pass


def main():
    '''Parameter is in config.ini'''
    config = configparser.ConfigParser()
    config.read('config.ini')
    main_paras = dict(config.items('main'))

    index = main_paras['structure_slice']

    traj = read(main_paras['structurefile'],
                index=index,
                format=main_paras['fileformat'])
    print("# of structures:", len(traj))

    constructor = calc_constructor(calc_type=config.get('main', 'calc_type'),
                                   calc_paras=config)

    index = str(index).split(':')

    # generate vasp_output.traj
    traj_saver = Trajectory('vasp_output.traj', 'w')

    # calc = constructor.get_calculator()
    for n, atoms in enumerate(traj):

        # atoms.set_calculator(calc)
        # atoms.get_forces()
        # atoms.get_potential_energy(force_consistent=True)
        # traj_saver.write(atoms)
        print('The No.{} job has been done.'.format(n))

        # save vasp output files
        dir_name = 'vasp_{}'.format(n)

        move_file('CHG', dir_name)
        move_file('CHGCAR', dir_name)
        move_file('CONTCAR', dir_name)
        move_file('DOSCAR', dir_name)
        move_file('EIGENVAL', dir_name)
        move_file('IBZKPT', dir_name)
        move_file('OSZICAR', dir_name)
        move_file('OUTCAR', dir_name)
        move_file('PCDAT', dir_name)
        move_file('POSCAR', dir_name)
        move_file('REPORT', dir_name)
        move_file('WAVECAR', dir_name)
        move_file('WDATCAR', dir_name)
        move_file('XDATCAR', dir_name)
        move_file('vasp.out', dir_name)
        move_file('vasprun.xml', dir_name)

    return


if __name__ == '__main__':
    # generate vasp_raw.traj
    vasp2traj()

    # call vasp api
    main()
