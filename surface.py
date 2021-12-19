from obj_loader import *
import gudhi as gd
import numpy as np
import math
import matplotlib.pyplot as plt

class Surface:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.st = gd.SimplexTree()
        
        self._input_file = ""
        self._output_file = self.input_file + "_out.csv"
        self._proj_dirs = [[0,0,1]]
        self._num_dirs = 0
        self._heights = []
        self._obj_loader = ObjLoader()
    
    def __init__(self, filename):
        self._input_file = filename
        self._obj_loader = ObjLoader(filename)

    def import_surface():
        if self._input_file == "":
            print("Please enter an input OBJ file name")
        else:
            _update_obj()
            _update_heights()
            _updata_st()
            
    def set_filename(self, filename):
        self._input_file = filename
        self._obj_loader = ObjLoader(filename)

    def set_proj_dirs(self, dirs):
        self._proj_dirs = dirs
        self._num_dirs = len(self._proj_dirs)
        self._normalize_dirs()

    def compute_persistence():
        self.st.compute_persistence(homology_coeff_field=2, persistence_dim_max=2)
    
    def _normalize_dirs():
        for i in range(len(self._proj_dirs)):
            norm = math.sqrt((self._proj_dirs[i][0])**2 
                    + (self._proj_dirs[i][1])**2
                    + (self._proj_dirs[i][2])**2)
            self._proj_dirs[i][0] = self._proj_dirs[i][0]/norm
            self._proj_dirs[i][1] = self._proj_dirs[i][1]/norm
            self._proj_dirs[i][2] = self._proj_dirs[i][2]/norm

    def _update_obj():
        self.vertices = self._obj_loader.vertices
        self.faces = self._obj_loader.faces
        f = len(self._obj_loader.faces)
        for i in range(f):
            for j in range(3):
                self.faces[i][j] = self.face[i][j]-1
        for i in range(f):
            self.st.insert(self.faces[i][:])

    def _update_heights(dir_ind = 0):
        direction = self._proj_dirs[dir_ind]
        self._heights = [0.0 for i in range(len(self.vertices))]
        for i in range(len(self.vertices)):
            self._heights[i] = direction[0]*self.vertices[i][0] +
                                direction[1]*self.vertices[i][1] +
                                direction[2]*self.vertices[i][2]

    def _update_st():
        v = len(self.vertices)
        for i in range(v):
            self.st.assign_filtration([i], height[i])
        
        for sk_value in self.st.get_skeleton(3):
            if len(sk_value[0]) == 2:
                self.st.assign_filtration(sk_value[0], max([height[sk_value[0][0]], 
                    height[sk_value[0][1]]]))
            if len(sk_value[0]) == 3:
                self.st.assign_filtration(sk_value[0], max([height[sk_value[0][0]], 
                    height[sk_value[0][1]], height[sk_value[0][2]]]))
