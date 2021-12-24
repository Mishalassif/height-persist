from core.surface import *
from core.manifold import *
from core.sphere_sampler import *

import faulthandler

faulthandler.enable()

surf = Surface()
surf.set_input_filename("bathtub_0001")
surf.update_surface()
print('Updated the surface')
surf._compute_persistence()
pd = surf.st.persistence(homology_coeff_field=2, persistence_dim_max=2)
print(pd)

surf.set_input_filename("../datasets/ModelNet10/chair/train/chair_0021", "off")
surf.update_surface()
print('Updated the surface')
surf._compute_persistence()
pd = surf.st.persistence(homology_coeff_field=2, persistence_dim_max=2)
print(pd)

#pdir = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [1,1,1], [1,1,-1]]
pdir = fibonacci_semisphere(4)
surf.set_proj_dirs(pdir)

'''
for i in range(len(pdir)):
    for j in range(surf._pl_num):
        plt.plot(surf._pl[0][i][0][j*surf._pl_res:(j+1)*surf._pl_res])
    plt.show()

for i in range(len(pdir)):
    for j in range(surf._pl_num):
        plt.plot(surf._pl[1][i][0][j*surf._pl_res:(j+1)*surf._pl_res])
    plt.show()
'''

'''
surf.set_input_filename("bathtub_0001", "off")
surf.update_surface()
surf.set_output_filename("output/bathtub_0001")
surf.output_pi()
surf.output_pl()

surf.set_input_filename("bathtub_0002", "off")
surf.update_surface()
surf.set_output_filename("output/bathtub_002")
surf.output_pi()
surf.output_pl()
'''
