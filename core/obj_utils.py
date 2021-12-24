import os
import math

class ObjLoader(object):
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        try:
            f = open(fileName)
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)

                    vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                    vertex = [round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2)]
                    self.vertices.append(vertex)

                elif line[0] == "f":
                    string = line.replace("//", "/")
                    ##
                    i = string.find(" ") + 1
                    face = []
                    for item in range(string.count(" ")):
                        if string.find(" ", i) == -1:
                            face.append(int(string[i:-1]))
                            break
                        face.append(int(string[i:string.find(" ", i)]))
                        i = string.find(" ", i) + 1
                    ##
                    self.faces.append(list(face))

            f.close()
        except IOError:
            print(".obj file not found.")

    def center_and_scale(self):
        mean = [0.0, 0.0, 0.0]
        for i in range(len(self.vertices)):
            for j in range(3):
                mean[j] = mean[j] + self.vertices[i][j]
        for j in range(3):
            mean[j] = mean[j]/(len(self.vertices))
        for i in range(len(self.vertices)):
            for j in range(3):
                self.vertices[i][j] = self.vertices[i][j] - mean[j]
        max_norm = 0.0
        for i in range(len(self.vertices)):
            max_norm = max(max_norm, math.sqrt(self.vertices[i][0]**2 +
                self.vertices[i][1]**2 + self.vertices[i][2]**2))
        for i in range(len(self.vertices)):
            for j in range(3):
                self.vertices[i][j] = self.vertices[i][j]/max_norm

def get_all_obj(root_dir):
    list_of_files = os.listdir(root_dir)
    list_of_obj = list()
    for entry in list_of_files:
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            list_of_obj = list_of_obj + get_all_obj(full_path)
        elif full_path[-4:] == '.obj':
            list_of_obj.append(full_path[:-4])
    return list_of_obj
