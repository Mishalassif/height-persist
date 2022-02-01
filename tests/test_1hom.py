import os
import math
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
list_obj = get_all_obj('../datasets/red-ModelNet10/bed')

pdir = fibonacci_semisphere(20)

for i in range(len(list_obj)):
    list_obj[i] = list_obj[i][12:]

surf = Surface()
surf.set_proj_dirs(pdir)

for obj_file in list_obj:
    surf.set_input_filename('../datasets/' + obj_file)
    surf.set_output_filename('../features/' + obj_file)
    surf.update_surface()
    surf._compute_persistence()
    #print(surf.st.persistence_intervals_in_dimension(2))
    #print(len(surf.st.persistence_intervals_in_dimension(2)))
    hom_pairs = surf.st.persistence_intervals_in_dimension(1)
    hom = 0
    for pair in hom_pairs:
        if pair[1] == math.inf:
            hom = hom+1
    #print("Homology of " obj_file + " is " + str(hom))
    print(hom)
