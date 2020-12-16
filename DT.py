
import pandas as pd

import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, explained_variance_score
from sklearn import cross_validation
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import r2_score
import imageio
import io 
import pydotplus
from itertools import product
#from scipy import misc 
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neighbors import KNeighborsClassifier

# =============================================================================
# Declaration of functions 
# =============================================================================
def AdaBoostedRegression(features, target, feature_names, plot_title):
    features_train, features_test, target_train, target_test = cross_validation.train_test_split(features, target, test_size=0.1)
    regressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4), n_estimators=50, random_state=0) #add random_state? 
    regressor.fit(features_train,target_train)

    score = regressor.score(features_train,target_train)
    
    #Evaluate performance of Adaboost regressor 
    target_pred = regressor.predict(features_test)
    mse = mean_squared_error(target_test,target_pred)
    evs = explained_variance_score(target_test,target_pred)
    print("\nADABOOST REGRESSOR")
    print("Mean squared error =", round(mse,2))
    print("Explained variance score =", round(evs,2))
    print("regressor score =", score)
    # extract features importances 
    feature_importances = regressor.feature_importances_
    # feature_names = comp_data.keys()

    #Normalize the importance values 
    feature_importances = 100.0 * (feature_importances / max(feature_importances))

    #sort the values and flip them 
    index_sorted = np.flipud(np.argsort(feature_importances))

    #arrange the X ticks
    pos = np.arange(index_sorted.shape[0]) + 0.5

    feature_name_sort = []
    for item in index_sorted:
        feature_name_sort.append(feature_names[item])
    
    feature_name_sort = np.array(feature_name_sort)
    
    #plot the bar graph 
    plt.figure()
    plt.bar(pos, feature_importances[index_sorted], align = 'center')
    plt.xticks(pos,feature_name_sort, rotation=45,ha='right',rotation_mode='anchor', fontsize = 12)
    indy=np.arange(0,120,step=20)
    plt.yticks(indy,fontsize=12)
    plt.ylabel ('Relative importance', fontsize = 12)
    plt.savefig(plot_title)
    plt.show()

    return feature_importances;

def show_tree(tree, features, path):
    f = io.StringIO()
    export_graphviz(tree, out_file=f, feature_names=features)
    pydotplus.graph_from_dot_data(f.getvalue()).write_png(path)
    img=imageio.imread(path)
    plt.rcParams["figure.figsize"]=(20,20)
    plt.imshow(img)
    return;


excel_file = 'summary_data_categorical.xlsx'
data = pd.read_excel(excel_file, header = 0)
data = data.drop(columns='simulation')
# =============================================================================
# Evaluate the influence of molecular features on LiF formation 
# =============================================================================

LiF = data['LiF_formation'].values
LiF = LiF[:,None]

new_names = ['LiF', 'Carbon$_{tol}$','Carbon$_{CF_3}$','-CF$_3$','-OCF$_3$','Facet','Presence$_{Salt}$','Salt$_{side}$','Bond break']
data.columns = new_names

mol_struc_features = ['Carbon$_{CF_3}$','-CF$_3$','-OCF$_3$','Facet','Presence$_{Salt}$']

data_mol = data[mol_struc_features]           
data_mol_value = data_mol.values     

# =============================================================================
# Try different regression and classification techniques
# =============================================================================
# Adaboosted regression
plot_title = 'Molecular Feature to LiF formation'
#tree = AdaBoostedRegression(data_mol_value, LiF, mol_struc_features, plot_title)

# decision tree regression
#regr = DecisionTreeRegressor(max_depth=4)
#dt=regr.fit(data_mol_value,LiF)
#show_tree(dt, mol_struc_features,'dt_RS.png')

# decision tree classification
clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=0)
dt = clf.fit(data_mol_value,LiF)
show_tree(dt, mol_struc_features,'dt_RS.png')
feature_importances = clf.feature_importances_
index_sorted = np.flipud(np.argsort(feature_importances))
feature_name_sort = []
for item in index_sorted:
    feature_name_sort.append(mol_struc_features[item])
feature_name_sort = np.array(feature_name_sort)
print('important feature: {}'.format(feature_name_sort))


