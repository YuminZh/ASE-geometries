# ASE-geometries-Bader analysis
- Bader analysis script is used to calcualte the charge transfer of the simulated geometries.
- In order to use this script, there are a few things need to be ready:
  1. The .dat file of the final simulated geometry. This can be produced using the Bader analysis code from GPAW package.
  2. The .dat and .xyz files of the surface slab, isolated electrolyte molecule and the isolated salt molecule. All these structures must already be relaxed. Again, the .dat file can be obatined from Bader analysis code from GPAW package.
- This script can handle the geometries with and without the salt molecule. However, it does not take more than two molecules. 
- This script can only interface with results produced from GPAW, in the sense that it takes the file formatting produced by GPAW program. 
- There is an example to demonstrate: ethylene carbonate-Li(100) interfacial interactions
  1. final_geomtry: EC_100_salt.dat
  2. DAT file of the surface: Li_100_ACF.dat
  3. xyz file of the surface: Li36.xyz
  4. DAT file of the molecule: EC.dat
  5. xyz file of the molecule: EC.xyz
  6. DAT file of the salt: F6LiP.dat
  7. xyz file of the salt: F6LiP.xyz
- The program is written in a way that interface with command line inputs. The program will ask questions, the user can just type in the correct file. 
