from surface import *


surf = Surface()
surf.set_filename("T149.obj")
surf.update_surface()
surf._compute_persistence()

'''
Right output: [(2, (0.24, inf)), (1, (-0.03, 0.06)), (0, (-0.15, inf)), (0, (-0.14, 0.04)), (0, (-0.01, 0.04)), (0, (-0.14, -0.13)), (0, (-0.14, -0.13))]
'''
pd = surf.st.persistence(homology_coeff_field=2, persistence_dim_max=2)
print(pd)

surf._output_header()
surf._output_pi()

pdir = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [1,1,1], [1,1,-1], []
surf.set_proj_dirs(pdir)
surf._output_header()
surf._output_pi()
pd = surf.st.persistence(homology_coeff_field=2, persistence_dim_max=2)

for i in range(len(pdir)):
    plt.imshow(np.flip(np.reshape(surf._pi[i][0], [surf._pi_res, surf._pi_res]), 0))
    plt.show()
