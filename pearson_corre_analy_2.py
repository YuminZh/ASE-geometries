"""

Pearson correlation analysis for fluorinated linear solvents

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# read in the collection of the data
excel_file = 'summary_data.xlsx'

# since my data has the first column assigned for simulated system names, 
# its' removed first 
data = pd.read_excel(excel_file, header = 0)
data_no_name = data.drop(columns='simulation')
# remove two more columns which are insignificant, determined by visualization
data_no_name = data_no_name.drop(columns={'C_CH3','O_CH3'})

# rename the columns of the data 
new_names = ['$\Delta G_{rxn}$','Li surface','Electrolyte','Salt', '$C_C$','$C_F$','$O_F$','$O_C$','$F_{CF_3}$','LiF', 
             'Carbon$_{tol}$','Carbon$_{CF_3}$','-$CF_3$','Facet','Presence$_{Salt}$']
data_no_name.columns = new_names
    
    
# some of the cases simulated have insiginificant reaction energy 
# because those reaction only involve chemisorption and physisorption
significant_cases = data_no_name[data_no_name['$\Delta G_{rxn}$']<-2]
# by visulization of the data, the cases with reaction energies lower than -2
# exclusively have the presence of the salt molecule.
significant_cases = significant_cases.drop(columns='Presence$_{Salt}$')


"""
  Start the calculation of pearson correaltion coefficients and plot 
  triangle heatmap 

"""
#pearsoncorr = data_no_name.corr(method = 'pearson')
pearsoncorr = significant_cases.corr(method = 'pearson')

# since we need to annotate the heatmap using strength of the correlation
# here, devide the strength to 4 categories
shape = pearsoncorr.shape
text = pearsoncorr
new_text = np.chararray((shape[0],shape[1]),itemsize = 1)
text_list = []
text_arr = []
for i in range(shape[0]):
    for j in range(shape[1]):
        if 0.8<text.iloc[i][j]<1 or -1<text.iloc[i][j]<-0.8:
            new_text[i][j] = 'S'
            text_list.append(new_text[i][j].decode('utf-8'))
        elif 0.4<text.iloc[i][j]<0.8 or -0.8<text.iloc[i][j]<-0.4:
            new_text[i][j] = 'M'
            text_list.append(new_text[i][j].decode('utf-8'))
        elif 0.2<text.iloc[i][j]<0.4 or -0.4<text.iloc[i][j]<-0.2:
            new_text[i][j] = 'W'
            text_list.append(new_text[i][j].decode('utf-8'))
        else:
            new_text[i][j] = 'N'
            text_list.append(new_text[i][j].decode('utf-8'))
    
    text_arr.append(text_list)
    text_list = []
    
text_arr = np.asarray(text_arr)        
fig,ax = plt.subplots()

# plot the half correlation map 
mask = np.zeros_like(pearsoncorr)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    f, ax = plt.subplots(figsize=(6, 5))
    ax = sns.heatmap(pearsoncorr, mask=mask, vmax=1,vmin = -1, square=True,
                     xticklabels=pearsoncorr.columns,
                     yticklabels=pearsoncorr.columns,
                     cmap='RdBu_r',
                     annot = text_arr,annot_kws={"size": 11}, fmt = '',
#                     cbar_kws={"ticks": ['strong','weak']},
                     
                     linewidth=1)

# the feature names along the X and Y axis  
ax.tick_params(labelsize = 8) 

# We want to show all ticks...
#ax.set_xticks(np.arange(text_arr.shape[0]))
#ax.set_yticks(np.arange(text_arr.shape[1]))

# no need to label the first feature label for y-axis and 
# last label for x-axis
y_labels = list(ax.get_yticklabels())
y_labels[0] = ' '

x_labels = list(ax.get_xticklabels())
x_labels[-1] = ' '

#ax.set_yticklabels(ax.get_yticklabels(),rotation=0)
#ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

ax.set_yticklabels(y_labels,rotation=0)
ax.set_xticklabels(x_labels, rotation=90)
ax.tick_params(axis='both', which='both',length=8 )

plt.savefig('correlation_sig.pdf',dpi=300,bbox_inches = "tight")
plt.close()
