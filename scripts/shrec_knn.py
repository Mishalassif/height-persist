import os
from core.surface import *
from core.sphere_sampler import *
from core.obj_utils import *

import sklearn

classes = ['alien', 'ants', 'armadillo', 'bird1', 'bird2', 'camel',
        'cat', 'centaur', 'dinosaur', 'dino_ske', 'dog1', 'dog2',
        'flamingo', 'glasses', 'gorilla', 'hand', 'horse', 'lamp',
        'man', 'myScissor', 'octopus', 'pliers', 'rabbit', 'santa',
        'shark', 'snake', 'spiders', 'two_balls', 'woman']

root_dir = '../datasets/shrec_16'

pdir = fibonacci_semisphere(20)

surf = Surface()
surf.set_proj_dirs(pdir)

feature_list = []
pl_dim = surf._pl_res*surf._pl_num

for i in range(len(classes)):
    list_obj = get_all_obj(root_dir + '/' + classes[i])
    for k in range(len(list_obj)):
        list_obj[k] = list_obj[k][len(root_dir + '/' + classes[i]):]
    for obj_file in list_obj:
        if obj_file[:5] == '/test':
            continue
        embedding = np.zeros((1, 2*20*pl_dim))
        surf.set_input_filename(root_dir + '/' + classes[i] + '/' + obj_file)
        surf.update_surface()
        for j in range(20):
            surf.compute_pl(j)
            embedding[0][2*j*pl_dim:(2*j+1)*pl_dim] = surf._pl[0][j][0]
            embedding[0][(2*j+1)*pl_dim:(2*j+2)*pl_dim] = surf._pl[1][j][0]
        feature_list.append((i,embedding))
        print('Featurized ' + obj_file + ' successfully !!!!')
    print('Completed featurizing ' + classes[i])
