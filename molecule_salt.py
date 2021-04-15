"""
Procedures: 
    
    1. Use Bader analysis to calculate the charge density and partial charges
       of each atom 
       
    2. Select the atoms that have the top five most highest partial charges 
    
    3. Select the atom that has the lowest partial charges
       procedure 2 and 3 excludes hydrogen atoms 
       
    4. Collect a list of vectors that contain point from the least negative to most negative atoms 
    
    5. Use these vectors to align the salt molecules 


"""
import numpy as np

from ase.io import read, write



def data_handle(file): # read the process the Bader analysis partial charge file ACF.dat
    
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

def high_low_charge_density_vectors(charges, positions):
    
    """
    - get the highest and lowest charges, locate the associated atoms 
    - use atoms to produce vectors 
    
    """
    # sort from the lowest to the highest 
    lst = len(charges) 

    for i in range(lst): 
          
        for j in range(0, lst-1): 
            if (float(charges[j][1]) > float(charges[j + 1][1])): 

                temp = charges[j] 

                charges[j]= charges[j + 1] 

                charges[j + 1]= temp 
    
    # check if the charge ranking is done correctly
    rank_charge_inspect(charges)
    
    # get atom positions and calculate vectors 
    # I used 3 top vectors, can add more if necessary

    num_vectors = 3
    
    low_atom_idx = int(charges[0][0])-1

    vectors = []
    
    high_atom_pos = []
    high_atom_idx = []
    
    for i in range(num_vectors):

        high_atom_idx.append(int(charges[-(i+1)][0])) # partial charge index, start from 1
        high_atom_pos.append(positions[int(charges[-(i+1)][0])-1]) # index for partial charge start with 1
        

    for item in high_atom_pos:
        diff = item - positions[low_atom_idx]
        vectors.append(diff)
        

    return vectors

def rank_charge_inspect(charges):
    
    check_lst = []
    for item in charges:
        check_lst.append(float(item[1]))
    
    min_idx = check_lst.index(min(check_lst))
    
    if min_idx != 0:
        
        print("partial charge ranking has error")
        print("the partial charge array is {}".format(charges))
    
    return 

def smart_translate(salt_unit_vec, mol_unit_vec, salt_atoms):
    
    # overlap the salt and solvent vectors first 
    dist = salt_unit_vec - mol_unit_vec
    salt_atoms.translate(dist)
    
    # find the span of solvent molecule in x,y,z directions 
    x_dir = []
    y_dir = []
    z_dir = []
    
    for item in mol_positions:
        x_dir.append(item[0])
        y_dir.append(item[1])
        z_dir.append(item[2])
    
    x_sp = max(x_dir) - min(x_dir)
    y_sp = max(y_dir) - min(y_dir)
    z_sp = max(z_dir) - min(z_dir)
    sps = [x_sp, y_sp, z_sp]
#    print('x_sp {}, y_sp {}, z_sp {}'.format(x_sp, y_sp, z_sp))
     
    shortest_sp = sps.index(min(sps))
    min_dist = 2.8
    # now move the salt molveuls about 3A in the direction where the span is the smallest 
    if shortest_sp == 0:
        trans = [min_dist,0,0]
    elif shortest_sp == 1:
        trans = [0,min_dist,0]
    else:
        trans = [0,0,min_dist]
        
    salt_atoms.translate(trans)
    
    return salt_atoms

# =============================================================================
#                            Start main program 
# =============================================================================
# read in files 
mol_charge_file = "C4H8O2_ACF.dat"
mol_atoms_file = "C4H8O2.traj"

salt_charge_file = "salt.dat"
salt_atoms_file = "salt.xyz" 


# Solvent Molecule: get the partial charges of each atom and calculate the top vectors 
# vector dierection, point from highest partial charge to lowest partial charge
mol_charges = data_handle(mol_charge_file)
mol_atoms = read(mol_atoms_file)

mol_symbols = mol_atoms.get_chemical_symbols()
mol_positions = mol_atoms.get_positions()
mol_vectors = high_low_charge_density_vectors(mol_charges,mol_positions)

# Salt molecule: get the partial charges of each atom and calculate the top vectors 
salt_charges = data_handle(salt_charge_file)
salt_atoms = read(salt_atoms_file)
salt_symbols = salt_atoms.get_chemical_symbols()
salt_positions = salt_atoms.get_positions()
salt_vectors = high_low_charge_density_vectors(salt_charges,salt_positions)

# the code will give three top vectors, but for salt, only need the first one
# and needs to be negated to align Li of salt with the highest energy-density of solvent
salt_vectors = salt_vectors[0]
salt_vectors = -salt_vectors 

# start align the salt molecule with the solvent molecule, first, find unit vectors
mol_unit_vec = mol_vectors / np.linalg.norm(mol_vectors, axis=-1)[:,None]
salt_unit_vec = salt_vectors /  np.linalg.norm(salt_vectors, axis=-1)

# Here is to pick top three solvent molecule vectors as reference for salt rotation 
for i in range(len(mol_unit_vec)):
    
    # make a copy of salt_atoms object, because each roation, it will start from the original salt molecule
    rot_salt = salt_atoms.copy()
    
    # keep a copy of original salt_vectors before rotation
    rot_salt_vectors = salt_vectors

    
    # rotate the salt molecule based on the solvent vectors 
    rot_salt.rotate(rot_salt_vectors, mol_unit_vec[i], center="COM")
    
    #now the salt is rotated, move it to the correct place respect to the solvent 
    trans_salt_atoms = smart_translate(rot_salt_vectors, mol_unit_vec[i], rot_salt)
    
    new_mol_atoms = mol_atoms.copy()
    salt_mol = new_mol_atoms.extend(trans_salt_atoms)
    salt_mol.write('salt_molecules_cluster_'+ str(i) +'.xyz')











# some useful matrix for other applications
#Rot,rmsd = R.align_vectors(mol_unit_vec[0][None,:], salt_unit_vec[None,:])
#rot_matrix = Rot.as_matrix()
#euler_angles = Rot.as_euler("xyz", degrees=True)
