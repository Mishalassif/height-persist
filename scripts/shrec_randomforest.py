import os
from core.surface import *
from core.sphere_sampler import *
from core.obj_utils import *

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

feature = 'pl'
test_model = True
classes = ['alien', 'ants', 'armadillo', 'bird1', 'bird2', 'camel',
        'cat', 'centaur', 'dinosaur', 'dino_ske', 'dog1', 'dog2',
        'flamingo', 'glasses', 'gorilla', 'hand', 'horse', 'lamp',
        'man', 'myScissor', 'octopus', 'pliers', 'rabbit', 'santa',
        'shark', 'snake', 'spiders', 'two_balls', 'woman']

classes = classes[:30]

#classes = ['alien', 'ants', 'armadillo', 'bird2']
#classes = ['alien', 'ants', 'armadillo', 'camel']
root_dir = '../datasets/shrec_16'

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
    for k in range(len(list_obj)):
        list_obj[k] = list_obj[k][len(root_dir + '/' + classes[i]):]
    for obj_file in list_obj:
        if obj_file[:5] == '/test':
            continue
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
        print('Featurized ' + obj_file + ' successfully !!!!')
    print('Completed featurizing ' + classes[i])

print('Completed featurizing train data')

model = RandomForestClassifier(random_state=1)
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
    
