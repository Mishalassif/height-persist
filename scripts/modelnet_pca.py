import os
import math
from core.surface import *
from core.sphere_sampler import *
from core.obj_utils import *

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier

feature = 'pi'
test_model = False
cv_model = True
online = False

def print(x):
    os.system('echo ' + '\'' + x + '\'')


classes = ['airplane', 'bathtub', 'bed', 'bench', 'bookshelf', 'bottle', 'bowl', 'car', 'chair', 'cone', 'cup', 'curtain', 'desk', 'door', 'dresser', 'flower_pot', 'glass_box', 'guitar', 'keyboard', 'lamp', 'laptop', 'mantel', 'monitor', 'night_stand', 'person', 'piano', 'plant', 'radio', 'range_hood', 'sink', 'sofa', 'stairs', 'stool', 'table', 'tent', 'toilet', 'tv_stand', 'vase', 'wardrobe', 'xbox']

root_dir = '../datasets/ModelNet40-2000'
feature_dir = '../features/ModelNet40-2000'

n_dirs = 20

pdir = fibonacci_semisphere(n_dirs)

surf = Surface()
surf.set_proj_dirs(pdir)

feature_list = []
label_list = []

if feature == 'pl':
    feature_dim = surf._pl_res*surf._pl_num
else:
    feature_dim = surf._pi_res*surf._pi_res

for i in range(len(classes)):
    list_obj = get_all_obj(root_dir + '/' + classes[i])
    count = 0
    for k in range(len(list_obj)):
        list_obj[k] = list_obj[k][len(root_dir + '/' + classes[i]):]
    for obj_file in list_obj:
        if obj_file[:5] == '/test':
            continue
        embedding = [0.0 for i in range(2*n_dirs*feature_dim)]
        if online == True:
            embedding = [0.0 for i in range(2*n_dirs*feature_dim)]
            surf.set_input_filename(root_dir + '/' + classes[i] + '/' + obj_file)
            surf.update_surface()
            for j in range(n_dirs):
                if feature == 'pl':
                    surf.compute_pl(j)
                    embedding[2*j*feature_dim:(2*j+1)*feature_dim] = surf._pl[0][j][0]
                    embedding[(2*j+1)*feature_dim:(2*j+2)*feature_dim] = surf._pl[1][j][0]
                else:
                    surf.compute_pi(j)
                    embedding[2*j*feature_dim:(2*j+1)*feature_dim] = surf._pi[0][j][0]
                    embedding[(2*j+1)*feature_dim:(2*j+2)*feature_dim] = surf._pi[1][j][0]
            feature_list.append(embedding)
            label_list.append(i)
        else:
            header_len = surf._header_len
            embedding = np.genfromtxt(feature_dir + '/' + classes[i] + obj_file + '_' + feature + '.csv', delimiter='\n', skip_header=header_len)
            #print(embedding)
            feature_list.append(embedding)
            label_list.append(i)
        count = count + 1
        print('Featurized ' + obj_file + '('+str(round(float(count/len(list_obj)),2)*100) +'%) successfully !!!!')
    print('Completed featurizing ' + classes[i])

print('Completed featurizing train data')

#model = RandomForestClassifier(random_state=1, n_estimators=100)
model = AdaBoostClassifier(random_state=1, n_estimators=100)
if cv_model == True:
    scores = cross_val_score(model, feature_list, label_list, cv=3)
    print("%0.2f 3-fold cv accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

if test_model == True:
    model.fit(feature_list, label_list)
    print('Random forest model fit on the whole of train data')
    test_feature_list = []
    test_label_list = []
    pred_label_list = []
    for i in range(len(classes)):
        list_obj = get_all_obj(root_dir + '/' + classes[i])
        for k in range(len(list_obj)):
            list_obj[k] = list_obj[k][len(root_dir + '/' + classes[i]):]
        for obj_file in list_obj:
            if obj_file[:5] != '/test':
                continue
            embedding = [0.0 for i in range(2*n_dirs*feature_dim)]
            if online == True:
                surf.set_input_filename(root_dir + '/' + classes[i] + '/' + obj_file)
                surf.update_surface()
                for j in range(n_dirs):
                    if feature == 'pl':
                        surf.compute_pl(j)
                        embedding[2*j*feature_dim:(2*j+1)*feature_dim] = surf._pl[0][j][0]
                        embedding[(2*j+1)*feature_dim:(2*j+2)*feature_dim] = surf._pl[1][j][0]
                    if feature == 'pi':
                        surf.compute_pi(j)
                        embedding[2*j*feature_dim:(2*j+1)*feature_dim] = surf._pi[0][j][0]
                        embedding[(2*j+1)*feature_dim:(2*j+2)*feature_dim] = surf._pi[1][j][0]
                test_feature_list.append(embedding)
                test_label_list.append(i)
                pred_label_list.append(model.predict([embedding]))
            else:
                header_len = surf._header_len
                embedding = np.genfromtxt(feature_dir + '/' + classes[i] + obj_file + '_' + feature + '.csv', delimiter='\n', skip_header=header_len)
                #print(embedding)
                test_feature_list.append(embedding)
                test_label_list.append(i)
                pred_label_list.append(model.predict([embedding]))
                #print(model.predict([embedding]))
            print('Featurized ' + obj_file + ' test data successfully !!!!')
        print('Completed featurizing ' + classes[i] + ' test data')

    correct_pred_list = []
    for element in zip(test_label_list, pred_label_list):
        if element[0] == element[1]:
            correct_pred_list.append(1)
        else:
            correct_pred_list.append(0)

    print("Accuracy on test set: " + str(sum(correct_pred_list)/len(correct_pred_list)))
    print(classification_report(test_label_list, pred_label_list, target_names=classes))

    
