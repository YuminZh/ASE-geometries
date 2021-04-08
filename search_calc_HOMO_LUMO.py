    
import re
import os 
import sys 
import numpy as np
import glob
from shutil import copyfile

import ase
from ase import *
from ase.io import read, write
from ase import Atoms
from gpaw import *
from gpaw import GPAW, PW, FermiDirac
from gpaw.eigensolvers import Davidson
from gpaw.poisson import PoissonSolver
from gpaw.test import equal
from myscripts import *
from gpaw.eigensolvers import RMMDIIS



path = os.getcwd()
#print("the current working directory is %s" % path)

def copy_file(file, sub_folder,):
    
    for sub_dir in sub_folder:
        
        copyfile(os.path.join(path + '/' + file), os.path.join(sub_dir, os.path.basename(file)))
        
    return 

def if_traj(file_name):
    
    traj = '.traj'
    if traj in file_name:
        return True

def write_xyz(root,item):
            
    os.chdir(root)
    
    name = item
    atoms = read(item)
    name = name[:-5]
    atoms.write(name+'.xyz')
    
    return

def if_gpw(file_name):
    
    gpw_file = '.gpw'
    if gpw_file in file_name:
        return True
    
    

def calc_eng_homo_lumo(atoms):
    
    # set gpaw calculator
    calc=GPAW(
    h=0.16,
    kpts=(1,1,1),
    xc='B3LYP',
    occupations=FermiDirac(width=0.1),
   # eigensolver=Davidson(3),
    eigensolver = RMMDIIS(),
    poissonsolver=PoissonSolver(eps=1e-12),
    maxiter=2000
    )
    
    atoms.calc = calc
    energy = atoms.get_potential_energy()
    print(energy)
    (homo, lumo) = calc.get_homo_lumo()  
    print("homo: {} and LUMO: {}".format(homo, lumo))
    return homo, lumo

def write_eng_homo_lumo(root,homo,lumo):
    os.chdir(root)
    f_out = open('homo_lumo.txt','w')
    f_out.write('homo:{} lumo:{}\n'.format(homo, lumo))
    
    return



# =============================================================================
# 
# =============================================================================


sub_folder = []
traj_all = []

# for homo lumo results
#f_out = open('energy_homo_lumo.txt','w')

for root, dirs, files in os.walk(path):
    sub_folder.append(root)
    
    for item in files:
        if if_traj(item) == True:
            write_xyz(root,item)
        elif if_gpw(item) == True:
            atoms = read(item)
            homo,lumo = calc_eng_homo_lumo(atoms)
            write_eng_homo_lumo(root, homo, lumo)
            
