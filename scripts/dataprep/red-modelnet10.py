import sys
import os
from core.off_utils import *

manifold_path = './manifold'
simplify_path = './simplify'

root_dir = '../../datasets/ModelNet10/bathtub/test'
tmp_file = 'tmp.obj'
tmp2_file = 'tmp2.obj'
list_off = get_all_off(root_dir)

print(list_off)

num_faces = 2000

count = 0.0
size = len(list_off)
for off_file in list_off:
    count = count+1.0
    os.system('meshlabserver -i ' + off_file + '.off' + ' -o ' + tmp_file)
    os.system(simplify_path + ' -i ' + tmp_file + ' -o ' + tmp2_file  + ' -m -f ' + str(num_faces))
    os.system(manifold_path + ' ' + tmp2_file + ' ' + off_file + '.obj')
    os.system(simplify_path + ' -i ' + off_file + '.obj' + ' -o ' + off_file + '.obj' + ' -m -f ' + str(num_faces))
    print("Done with " + str(round(float(count)/size, 2)*100) + "%")
