import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

from modelnet40_pi import ModelNet40PI

train_data = ModelNet40PI(
    root="/home/mishal2/height-persist/features/red_ModelNet40",
    train=True
)

test_data = ModelNet40PI(
    root="/home/mishal2/height-persist/features/red_ModelNet40",
    train=False
)


train_dataloader = DataLoader(train_data, batch_size=1, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=1, shuffle=True)

train_features, train_labels = next(iter(train_dataloader))
print(f"Feature batch shape: {train_features.size()}")
print(f"Labels batch shape: {train_labels.size()}")
img = train_features[0][0].squeeze()
label = train_labels[0]
plt.imshow(img, cmap="gray")
plt.savefig('test.png')
print(f"Label: {label}")
