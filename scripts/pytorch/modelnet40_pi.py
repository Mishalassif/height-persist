import pandas as pd
import numpy as np
from PIL import Image

from torchvision import transforms
from torch.utils.data.dataset import Dataset 
import torch
class ModelNet40PI(Dataset):
    def __init__(self, root, train, height=20, width=20, channels=40, header_len=26, transform=None):
        """
        Custom dataset example for reading image locations and labels from csv
        but reading images from files
        Args:
            csv_path (string): path to csv file
        """
        self.root = root
        csv_path = root + "/modelnet40_"
        if train == True:
            csv_path = csv_path + "train.csv"
        else:
            csv_path = csv_path + "test.csv"
        self.data_info = pd.read_csv(csv_path, header=None)
        self.image_arr = np.asarray(self.data_info.iloc[:, 0])
        self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        self.data_len = len(self.data_info.index)

        self.height = height
        self.width = width
        self.channels = channels
        self.header_len = header_len

    def __getitem__(self, index):
        single_image_name = self.root + '/' + self.image_arr[index]
        img_as_arr = np.loadtxt(single_image_name, skiprows=self.header_len)
        img_as_tensor = torch.from_numpy(img_as_arr)
        img_as_tensor = torch.reshape(img_as_tensor, (self.channels, self.height, self.width))

        # Get label(class) of the image based on the cropped pandas column
        single_image_label = self.label_arr[index]
        return (img_as_tensor, single_image_label)

    def __len__(self):
        return self.data_len

