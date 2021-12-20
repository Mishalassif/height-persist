from surface import *
from sphere_sampler import *

surf = Surface()
surf.set_input_filename("T149")
surf.update_surface()
surf._compute_persistence()
'''
Right output(149): [(2, (0.24, inf)), (1, (-0.03, 0.06)), (0, (-0.15, inf)), (0, (-0.14, 0.04)), (0, (-0.01, 0.04)), (0, (-0.14, -0.13)), (0, (-0.14, -0.13))]

'''
pd = surf.st.persistence(homology_coeff_field=2, persistence_dim_max=2)
print(pd)

surf.set_input_filename("T124")
surf.update_surface()
surf.set_output_directory("output/")
surf._compute_persistence()
'''
Right output(124): [(2, (0.31, inf)), (1, (0.25, inf)), (1, (0.24, inf)), (1, (-0.02, 0.27)), (1, (0.04, 0.3)), (1, (-0.01, 0.22)), (1, (0.02, 0.24)), (1, (-0.03, 0.15)), (1, (0.15, 0.27)), (1, (0.16, 0.28)), (1, (0.08, 0.15)), (1, (-0.01, 0.03)), (1, (0.17, 0.2)), (1, (0.08, 0.1)), (1, (-0.63, -0.62)), (1, (0.08, 0.09)), (0, (-0.67, inf)), (0, (-0.1, -0.03)), (0, (-0.36, -0.3)), (0, (0.22, 0.24))]
'''
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

surf.set_input_filename("T149")
surf.update_surface()
surf.set_output_directory("output/")
surf.output_pi()
surf.output_pl()

surf.set_input_filename("T124")
surf.update_surface()
surf.set_output_directory("output/")
surf.output_pi()
surf.output_pl()
