import os
import string

class OffLoader(object):
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        try:
            f = open(fileName)
            print('File open')
            line_counter = 0
            num_v = 0
            num_f = 0
            for line in f:
                if line_counter == 0:
                    line_counter = line_counter + 1
                    continue
                elif line_counter == 1:
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    num_v = int(line[:index1])
                    num_f = int(line[index1:index2])
                    print("Number of vertices: " + str(num_v))
                    print("Number of faces: " + str(num_f))
                    line_counter = line_counter + 1
                    continue
                
                if line_counter <= 1 + num_v:
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    print(line)
                    vertex = (float(line[:index1]), float(line[index1:index2]), float(line[index2:index3]))
                    vertex = [round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2)]
                    self.vertices.append(vertex)
                else:
                    string = line.replace("//", "/")
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
                line_counter = line_counter + 1
                print('Line counter updated to ' + str(line_counter))
            f.close()
        except IOError:
            print(".off file not found.")

def get_all_off(root_dir):
    list_of_files = os.listdir(root_dir)
    list_of_obj = list()
    for entry in list_of_files:
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            list_of_obj = list_of_obj + get_all_obj(full_path)
        elif full_path[-4:] == '.off':
            list_of_obj.append(full_path[:-4])
    return list_of_obj
