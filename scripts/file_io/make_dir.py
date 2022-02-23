import os

list_dir = os.listdir('./ModelNet40')
for entry in list_dir:
    if os.path.isdir(entry):
        full_path = os.path.join('./ModelNet40_obj', entry[12:])
        os.mkdir(full_path)
