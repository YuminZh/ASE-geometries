# =============================================================================
# This script is to add the molecule on top of the surface 
# Before using, we should have the .traj file for the surface slab and .traj file
# of the molecule file, this currently cannot handle salt molecule 
# it will normalize the mass of the molecule in order to get a position center 
# later on, will implement the height adjustment for adding molecule on surface
# =============================================================================

from ase.io import read, write
from ase.visualize import view
from ase.build import add_adsorbate
import glob
import math

# read in the surface file and molecule file                                                                                              
surface = glob.glob('Li*.traj')[0]# Li slab specific                                                                                      
atoms = glob.glob('C*.traj')[0]# molecule always contain and start with Carbon                                                            

# read files into ase                                                                                                                     
surface = read(surface)
atoms = read(atoms)

# find the location of X-Y center of surface slab                                                                                         
# find the center mass of molecule                                                                                                        

surface_array = surface.get_cell()
surface_x = surface_array[0][0]/2
surface_y = surface_array[1][1]/2
print("x and y lenth: {}, {}".format(surface_x, surface_y))


atoms.center()
atom_positions = atoms.get_positions()
atoms_array_shape = atom_positions.shape
# make an array of size of the number of atoms in the molecule, filled with 1                                                             
# to normalize masses                                                                                                                     
norm_mass = [1]*atoms_array_shape[0]
atoms.set_masses(norm_mass)
center_mass = atoms.get_center_of_mass()



# calculate which atom has the shortest distance compare to center mass of molecule                                                       

euc_dis_all = []
for pos in atom_positions:
    dis = pos - center_mass
    euc_dis = math.sqrt(dis[0]**2 + dis[1]**2 + dis[2]**2)
    euc_dis_all.append(euc_dis)
    euc_dis_all.append(euc_dis)

min_euc = min(euc_dis_all)
atom_idx_center = euc_dis_all.index(min_euc)
print('min_idx: {}'.format(atom_idx_center))

# perform the absorption                                                                                                                  
add_adsorbate(surface, atoms, 3, (surface_x, surface_y), None, atom_idx_center)

surface.center()

surface.write('surf_atoms.traj')