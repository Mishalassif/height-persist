from obj_loader import *

import gudhi as gd
import gudhi.representations

import numpy as np
import math
import csv
import matplotlib.pyplot as plt

class Surface:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.st = gd.SimplexTree()
        
        self._input_file = ""
        self._output_file = self._input_file + "_out.csv"
        self._output_dir = ""
        self._proj_dirs = [[0,0,1]]
        self._num_dirs = 0
        self._heights = []

        self._pi_bw = 1e-2
        self._pi_res = 50
        self._pi_max = 0.4
        self._pi_min = -0.4
        '''
        self._pi_max = 1.0
        self._pi_min = -1.0
        '''
        self._pi = [[0.0 for i in range(len(self._proj_dirs))] for j in range(2)]

        self._pl_res = 100
        self._pl_num = 5
        self._pl = [[0.0 for i in range(len(self._proj_dirs))] for j in range(2)]


    def _output_header(self, output_file):
        with open(output_file, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(["==Header begins=="])
            csvwriter.writerow(["PI bw", "PI res", "PI max", "PI min"])
            csvwriter.writerow([self._pi_bw, self._pi_res, self._pi_max, self._pi_min])
            csvwriter.writerow(["Projection directions"])
            for row in self._proj_dirs:
                csvwriter.writerow(row)
            csvwriter.writerow(["==Header ends=="])
            csvwriter.writerow([])
    
    def _compute_persistence(self):
        self.st.compute_persistence(homology_coeff_field=2, persistence_dim_max=2)
        
    def _normalize_dirs(self):
        for i in range(len(self._proj_dirs)):
            norm = math.sqrt((self._proj_dirs[i][0])**2 
                    + (self._proj_dirs[i][1])**2
                    + (self._proj_dirs[i][2])**2)
            self._proj_dirs[i][0] = self._proj_dirs[i][0]/norm
            self._proj_dirs[i][1] = self._proj_dirs[i][1]/norm
            self._proj_dirs[i][2] = self._proj_dirs[i][2]/norm

    def _update_obj(self):
        self.vertices = self._obj_loader.vertices
        self.faces = self._obj_loader.faces
        f = len(self._obj_loader.faces)
        for i in range(f):
            for j in range(3):
                self.faces[i][j] = self.faces[i][j]-1
        for i in range(f):
            self.st.insert(self.faces[i][:])

    '''
    A call to this function should be followed by a call to _update_st()
    '''
    def _update_heights(self, dir_ind = 0):
        direction = self._proj_dirs[dir_ind]
        self._heights = [0.0 for i in range(len(self.vertices))]
        for i in range(len(self.vertices)):
            self._heights[i] = direction[0]*self.vertices[i][0]+direction[1]*self.vertices[i][1]+direction[2]*self.vertices[i][2]

    def _update_st(self):
        v = len(self.vertices)
        for i in range(v):
            self.st.assign_filtration([i], self._heights[i])
        
        for sk_value in self.st.get_skeleton(3):
            if len(sk_value[0]) == 2:
                self.st.assign_filtration(sk_value[0], max([self._heights[sk_value[0][0]], 
                    self._heights[sk_value[0][1]]]))
            if len(sk_value[0]) == 3:
                self.st.assign_filtration(sk_value[0], max([self._heights[sk_value[0][0]], 
                    self._heights[sk_value[0][1]], self._heights[sk_value[0][2]]]))

    def _clear_st(self):
        self.st = gd.SimplexTree()

    def update_surface(self):
        if self._input_file == "":
            print("Please enter an input OBJ file name")
        else:
            self._clear_st()
            self._update_obj()
            self._update_heights()
            self._update_st()
            
    def set_input_filename(self, filename):
        self._input_file = filename
        self._obj_loader = ObjLoader(filename+".obj")
        self._output_file = self._input_file

    def set_output_filename(self, filename):
        self._output_file = filename

    def set_proj_dirs(self, dirs):
        self._proj_dirs = dirs
        self._num_dirs = len(self._proj_dirs)
        self._normalize_dirs()
        self._pi = [[0.0 for i in range(len(self._proj_dirs))] for j in range(2)]
        self._pl = [[0.0 for i in range(len(self._proj_dirs))] for j in range(2)]

    def compute_pi(self,i):
        self._update_heights(i)
        self._update_st()
        self._compute_persistence()

        preproc = gd.representations.preprocessing.DiagramSelector(use=True, limit=1000)
        PI = gd.representations.PersistenceImage(bandwidth=self._pi_bw, weight=lambda x: x[1]**2, \
                                                im_range=[self._pi_min,self._pi_max,self._pi_min,self._pi_max], resolution=[self._pi_res,self._pi_res])
        if len(preproc.transform([self.st.persistence_intervals_in_dimension(0)])[0]) == 0:
            self._pi[0][i] = [np.zeros((1, self._pi_res*self._pi_res))]
        else:
            self._pi[0][i] = PI.fit_transform(preproc.transform([self.st.persistence_intervals_in_dimension(0)]))
        if len(preproc.transform([self.st.persistence_intervals_in_dimension(1)])[0]) == 0:
            self._pi[1][i] = [np.zeros((1, self._pi_res*self._pi_res))]
        else:
            self._pi[1][i] = PI.fit_transform(preproc.transform([self.st.persistence_intervals_in_dimension(1)]))
        '''
        plt.imshow(np.flip(np.reshape(self._pi[0][i][0], [self._pi_res,self._pi_res]), 0))
        plt.title("Persistence Image")
        plt.show()
        '''

    def compute_pl(self,i):
        self._update_heights(i)
        self._update_st()
        self._compute_persistence()

        preproc = gd.representations.preprocessing.DiagramSelector(use=True, limit=1000)
        PL = gd.representations.Landscape(num_landscapes=self._pl_num, resolution=self._pl_res)
        if len(preproc.transform([self.st.persistence_intervals_in_dimension(0)])[0]) == 0:
            self._pl[0][i] = np.zeros((1, self._pl_res*self._pl_num))
        else:
            #print(self.st.persistence_intervals_in_dimension(0))
            self._pl[0][i] = PL.fit_transform(preproc.transform([self.st.persistence_intervals_in_dimension(0)]))
        if len(preproc.transform([self.st.persistence_intervals_in_dimension(1)])[0]) == 0:
            self._pl[1][i] = np.zeros((1, self._pl_res*self._pl_num))
        else:
            self._pl[1][i] = PL.fit_transform(preproc.transform([self.st.persistence_intervals_in_dimension(1)]))
        '''
        plt.plot(self._pl[0][i][0][:self._pl_res])
        plt.plot(self._pl[0][i][0][self._pl_res:2*self._pl_res])
        plt.title("Landscape")
        plt.show()
        '''
    
    def output_pi(self):
        output_file = self._output_file + "_pi.csv"
        self._output_header(output_file)
        with open(output_file, "a") as csvfile:
            csvwriter = csv.writer(csvfile) 
            for i in range(len(self._proj_dirs)):
                self.compute_pi(i)
                np.savetxt(csvfile, np.reshape(self._pi[0][i][0], [self._pi_res, self._pi_res]))
                csvwriter.writerow(["=====PI====="])

    def output_pl(self):
        output_file = self._output_file + "_pl.csv"
        self._output_header(output_file)
        with open(output_file, "a") as csvfile:
            csvwriter = csv.writer(csvfile) 
            for i in range(len(self._proj_dirs)):
                self.compute_pl(i)
                np.savetxt(csvfile, np.reshape(self._pl[0][i][0], [self._pl_num, self._pl_res]))
                csvwriter.writerow(["=====PL====="])

