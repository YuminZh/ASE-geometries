
import sys
import os
import pathlib
import os.path
# =============================================================================
# functions 
# =============================================================================
def data_handle(file):
    
    with open(file) as f:
        
        data = []
        for line in f:
            line_data = line.split()
            data.append(line_data)
    
    del data[0:2]
    for line in data: 
        del line[1:4]
        del line[2:6]
    data = data[:-4]   
    
    return data

def get_element(xyz_file):
    
    with open(xyz_file) as f:
        element = []
        for line in f:
            line_data = line.split()
            ele = line_data[0]
            element.append(ele)
    element = element[2:]
              
    return element

def make_initial_charge_dict(file_ACF, file_xyz, data_dict, component, idx):
    
    """ 
    obtain the element name from the .xyz file
    obtain the charge density data from the .ACF file
    make a dictionary for the simulation component: surface slab, electrolyte molecule
    and/or the salt molecule
    """
    element = get_element(file_xyz)
    element_idx = 0
    
    data_ACF = data_handle(file_ACF)
    
    data_dict[component] = {}

    for line in data_ACF: 
        data_dict[component][idx + int(line[0])-1] = {element[element_idx], float(line[1])}
        element_idx += 1
    comp_idx = idx + len(data_dict[component])
    
    return data_dict[component], comp_idx

def final_charge_change_dict(file_ACF, initial_data_dict, surf_idx, mol_idx, salt_idx):
    
    """
    initialize the variables for use 
    
    """
    data_dict = {}
    ini_idx = 0 # this is for using in the for loop later
    
    if salt_idx == False:
        idx_collect = (ini_idx, surf_idx, mol_idx)
        components = ('surf_slab', 'mol')
    else:
        idx_collect = (ini_idx, surf_idx, mol_idx, salt_idx)
        components = ('surf_slab', 'mol', 'salt')
        
    final_charge_change = {}  
    
    """
    obtain the charge distribution data of the simulated geometry
    
    """
    final_charge = data_handle(file_ACF) # the index starts from 1
    
    
    """
    calculate the charge differences and input them to a dictionary
    
    """
    for i in range(len(components)):
        data_dict[components[i]] = {} # create a sub dictionary
        total_diff = 0
 
        print(idx_collect[i])
        for j in range(idx_collect[i],idx_collect[i+1]):
            # initial_data_dict[components[i]][j] is a set, need to sort to access the element name value, 
            element_name = sorted(initial_data_dict[components[i]][j], key=str) 
            # the charge density change from initial separated geometry to final simulated geometry
            charge_diff = float(final_charge[j][1]) - element_name[0] 
            data_dict[components[i]][j] = {element_name[1], charge_diff}
            total_diff = total_diff + charge_diff
        # the charge transfer for the specific component of the geometry (surf, mol or salt)   
        final_charge_change[components[i]] = {total_diff}
           
    return data_dict, final_charge_change


# =============================================================================
# example system input if using a command arguments input  
# =============================================================================
#
#final_data = sys.argv[1]
#surf_ACF = sys.argv[2]
#surf_xyz = sys.argv[3]
#mol_ACF = sys.argv[4]
#mol_xyz = sys.argv[5]
#salt_ACF = sys.argv[6]
#salt_xyz = sys.argv[7]

"""

    An example of the command line input for the system containing EC, salt, and 
    Li(100) surface

    final_data = "EC_100_salt.dat"
    surf_ACF = "Li_100_ACF.dat"
    surf_xyz = "Li36.xyz"
    mol_ACF = "EC.dat"
    mol_xyz = "EC.xyz"
    salt_ACF = "F6LiP.dat"
    salt_xyz = "F6LiP.xyz"
    
    
"""
f_out = open('charge_trans_data.txt','w')
# =============================================================================
#  the charge distribution for isolated components 
# =============================================================================

    
salt_answer = input("is salt molecule included in the simulation?")
yes = {'yes', 'y'}
no = {'no','n'}

if salt_answer in yes:
    final_data = input('-input the .dat file for the simulated geometry composed of surface, electrolyte with the salt:')
    surf_ACF = input('-input the .dat file of the isolated surface slab:')
    surf_xyz = input('-input the .xyz file of the isolated surface slab:')
    mol_ACF = input('-input the .dat file of the isolated electrolyte molecule:')
    mol_xyz = input('-input the .xyz file of the isolated electrolyte molecule:')
    
    salt_ACF = input('-input the .dat file for the isolated salt molecule:')
    salt_xyz = input('-input the .xyz file for the isolated salt molecule:')          
        
    initial_data_dict = {}
    
    dict_surf, surf_idx = make_initial_charge_dict(surf_ACF, surf_xyz, initial_data_dict, 'surf_slab', 0)
    
    dict_mol, mol_idx = make_initial_charge_dict(mol_ACF, mol_xyz, initial_data_dict, 'mol', surf_idx)
    
    dict_salt, salt_idx = make_initial_charge_dict(salt_ACF, salt_xyz, initial_data_dict, 'salt', mol_idx)
    
    # the initial data dict contains the charge density of the isolated components
    
    # =============================================================================
    # the final charge transfer compare to the initial geometry
    # =============================================================================
    
    charge_trans, total_charge_change = final_charge_change_dict(final_data, initial_data_dict, surf_idx, mol_idx, salt_idx)

    print(total_charge_change)
    
elif salt_answer in no:
    final_data = input('-input the .dat file for the simulated geometry composed of surface, electrolyte without salt:')
    surf_ACF = input('-input the .dat file of the isolated surface slab:')
    surf_xyz = input('-input the .xyz file of the isolated surface slab:')
    mol_ACF = input('-input the .dat file of the isolated electrolyte molecule:')
    mol_xyz = input('-input the .xyz file of the isolated electrolyte molecule:')
    
    initial_data_dict = {}
    
    dict_surf, surf_idx = make_initial_charge_dict(surf_ACF, surf_xyz, initial_data_dict, 'surf_slab', 0)
    
    dict_mol, mol_idx = make_initial_charge_dict(mol_ACF, mol_xyz, initial_data_dict, 'mol', surf_idx)
    
    charge_trans, total_charge_change = final_charge_change_dict(final_data, initial_data_dict, surf_idx, mol_idx, salt_idx = False)
    
    print(total_charge_change)
    
# =============================================================================
# Write all charge transfer changes into a file 
# =============================================================================
for key,val in charge_trans.items():
    f_out.write('component: {}---------------------------\n'.format(key))
    f_out.write('idx, charge change, element\n')
    for idx,change in val.items():
        change = sorted(change, key=str)
        f_out.write('{}, {}\n'.format(idx, change))
  
