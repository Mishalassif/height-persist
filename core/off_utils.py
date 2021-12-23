import os

class OffLoader(object):
    def __init__(self, fileName):
        self.vertices = []
        self.faces = []
        self.edges = []
        try:
            f = open(fileName)
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
                    line_counter = line_counter + 1
                    continue
                
                if line_counter <= 1 + num_v:
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    vertex = (float(line[:index1]), float(line[index1:index2]), float(line[index2:index3]))
                    vertex = [round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2)]
                    self.vertices.append(vertex)
                else:
                    index1 = line.find(" ") + 1
                    index2 = line.find(" ", index1 + 1)
                    index3 = line.find(" ", index2 + 1)
                    if int(line[0]) == 3:
                        face = [int(line[index1:index2]), int(line[index2:index3]), int(line[index3:])]
                        self.faces.append(face)
                    elif int(line[0]) == 2:
                        edge = [int(line[index1:index2]), int(line[index2:index3])]
                        self.edges.append(edge)
                    '''
                    for item in range(string.count(" ")):
                        if string.find(" ", i) == -1:
                            face.append(int(string[i:-1]))
                            break
                        face.append(int(string[i:string.find(" ", i)]))
                        i = string.find(" ", i) + 1
                    ##
                    '''
                line_counter = line_counter + 1
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
