import os
from core.surface import *
from core.sphere_sampler import *
from core.obj_utils import *

root_dir = '../datasets'
features_dir = '../features'

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
pdir = fibonacci_semisphere(1)

for i in range(len(list_obj)):
    list_obj[i] = list_obj[i][12:]

surf = Surface()
surf.set_proj_dirs(pdir)

cont = ''
cont = input("About to overwrite the features folder, are you sure you want to continue? (y/n)")

if cont == 'y':
    for obj_file in list_obj:
        surf.set_input_filename('../datasets/' + obj_file)
        surf.set_output_filename('../features/' + obj_file)
        surf.update_surface()
        surf.output_pi()
        surf.output_pl()
        print('Featurized ' + obj_file + ' successfully !!!!')
else:
    print("Aborting")
