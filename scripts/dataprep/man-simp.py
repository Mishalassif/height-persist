import sys
import os

manifold_path = '/home/mishal/Documents/Code/Mesh/height-persist/scripts/dataprep/manifold'
simplify_path = '/home/mishal/Documents/Code/Mesh/height-persist/scripts/dataprep/simplify'

input_file = sys.argv[1]
output_file = sys.argv[2]

num_faces = 2000

os.system(manifold_path + ' ' + input_file + ' ' + output_file)
os.system(simplify_path + ' -i ' + output_file + ' -o ' + output_file + ' -m -f ' + str(num_faces))
