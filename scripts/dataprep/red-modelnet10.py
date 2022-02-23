import sys
import os
from core.obj_utils import *

#obj_class = sys.argv[1]

manifold_path = './manifold'
simplify_path = './simplify'

#root_dir = '../../datasets/ModelNet40_obj/'+obj_class
root_dir = '../../datasets/Unreduced_ModelNet40'
tmp_file = 'tmp.obj'
tmp2_file = 'tmp2.obj'
list_obj = get_all_obj(root_dir)

#print(list_off)

num_faces = 2000

count = 0.0
size = len(list_obj)
for obj_file in list_obj:
    count = count+1.0
    #print(simplify_path + ' -i ' + obj_file + '.obj'  + ' -o ' + obj_file + '_red.obj'  + ' -m -f ' + str(num_faces))
    os.system('timeout -s SIGINT 30m ' + manifold_path + ' ' + obj_file + '.obj'  + ' ' + obj_file + '_tmp.obj')
    os.system('timeout -s SIGINT 30m ' + simplify_path + ' -i ' + obj_file + '_tmp.obj'  + ' -o ' + obj_file + '_red.obj'  + ' -m -f ' + str(num_faces))
    os. system("echo \" Done with " + str(round(float(count)/size, 2)*100) + "% \" ")
