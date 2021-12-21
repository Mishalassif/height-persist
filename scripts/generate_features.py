import os
from core.surface import *
from core.sphere_sampler import *

root_dir = '../datasets'
features_dir = '../features'

def get_all_obj(root_dir):
    list_of_files = os.listdir(root_dir)
    list_of_obj = list()
    for entry in list_of_files:
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            list_of_obj = list_of_obj + get_all_obj(full_path)
        elif full_path[-4:] == '.obj':
            list_of_obj.append(full_path[:-4])
    return list_of_obj

def create_feature_dir(root_dir = '../datasets', features_dir = '../features'):
    if os.path.isdir(features_dir) == False:
        os.mkdir(features_dir)
    list_of_dir = os.listdir(root_dir)
    for subdir in list_of_dir:
        full_path = os.path.join(root_dir, subdir)
        full_feature_path = os.path.join(features_dir, subdir)
        if os.path.isdir(full_path):
            if os.path.isdir(full_feature_path) == False:
                os.mkdir(full_feature_path)
            create_feature_dir(full_path, full_feature_path)

create_feature_dir()
list_obj = get_all_obj('../datasets/shrec_16')

print(list_obj)
pdir = fibonacci_semisphere(4)

for i in range(len(list_obj)):
    list_obj[i] = list_obj[i][12:]

surf = Surface()
surf.set_proj_dirs(pdir)

for obj_file in list_obj:
    surf.set_input_filename('../datasets/' + obj_file)
    surf.set_output_filename('../features/' + obj_file)
    surf.update_surface()
    surf.output_pi()
    surf.output_pl()
    print('Featurized ' + obj_file + ' successfully !!!!')
