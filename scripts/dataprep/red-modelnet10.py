import sys
import os
from core.off_utils import *

manifold_path = './manifold'
simplify_path = './simplify'

root_dir = '../../datasets/ModelNet10/toilet'
tmp_file = 'tmp.obj'
list_off = get_all_off(root_dir)

print(list_off)

num_faces = 2000

for off_file in list_off:
    os.system('meshlabserver -i ' + off_file + '.off' + ' -o ' + tmp_file)
    os.system(manifold_path + ' ' + tmp_file + ' ' + off_file + '.obj')
    os.system(simplify_path + ' -i ' + off_file + '.obj' + ' -o ' + off_file + '.obj' + ' -m -f ' + str(num_faces))
