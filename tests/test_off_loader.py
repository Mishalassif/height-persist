from core.off_utils import *

off_loader = OffLoader('../datasets/ModelNet10/bathtub/train/bathtub_0010.off')

print(off_loader.vertices)
print(off_loader.faces)
print(len(off_loader.vertices))
print(len(off_loader.faces))
