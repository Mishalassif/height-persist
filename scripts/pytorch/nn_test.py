import os
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torch.utils.data import DataLoader, ConcatDataset
from torchvision import transforms
from torch import nn

from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

import matplotlib.pyplot as plt

from modelnet40_pi import ModelNet40PI

def print(string):
    os.system('echo ' + "\'" + string + "\'")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Device: ' + str(device))

train_data = ModelNet40PI(
    root="/home/mishal2/height-persist/features/red_ModelNet40",
    train=True
)

test_data = ModelNet40PI(
    root="/home/mishal2/height-persist/features/red_ModelNet40",
    train=False
)

testloader = torch.utils.data.DataLoader(
                  test_data,
                  batch_size=800, shuffle=True)
print('Completed loading data')

class ConvNet(nn.Module):
    '''
    Simple Convolutional Neural Network
    '''
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(40, 20, kernel_size=3),
            nn.MaxPool2d(kernel_size = 2),
            nn.ReLU(),
            #nn.Dropout(p=0.2),
            nn.Conv2d(20, 10, kernel_size=3),
            nn.MaxPool2d(kernel_size = 2),
            nn.ReLU(),
            #nn.Dropout(p=0.2)  ,
            nn.Flatten(),
            nn.Linear(10*3*3, 50),
            nn.ReLU(),
            #nn.Dropout(p=0.2),
            nn.Linear(50, 40),
            nn.Softmax(dim=1)
            )

    def forward(self, x):
        return self.layers(x)

loss_function = nn.CrossEntropyLoss()

k_folds = 3
num_epochs = 40
kfold = KFold(n_splits=k_folds, shuffle=True)
#kfold = StratifiedKFold(n_splits=k_folds, shuffle=True)

dataset = train_data

results = {}

BATCH_SIZE = 50
def reset_weights(m):
  '''
    Try resetting model weights to avoid
    weight leakage.
  '''
  for layer in m.children():
   if hasattr(layer, 'reset_parameters'):
    print('Reset trainable parameters of layer = ' + str(layer))
    layer.reset_parameters()

for fold, (train_ids, test_ids) in enumerate(kfold.split(dataset)):

    print('FOLD ' + str(fold))
    print('--------------------------------')

    train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
    test_subsampler = torch.utils.data.SubsetRandomSampler(test_ids)

    trainloader = torch.utils.data.DataLoader(
                      dataset,
                      batch_size=BATCH_SIZE, sampler=train_subsampler)
    testloader = torch.utils.data.DataLoader(
                      dataset,
                      batch_size=BATCH_SIZE, sampler=test_subsampler)

    network = ConvNet()
    network = network.double()
    network = network.to(device)
    network.apply(reset_weights)

    optimizer = torch.optim.Adam(network.parameters())

    for epoch in range(0, num_epochs):

      print('Starting epoch ' + str(epoch+1))

      current_loss = 0.0

      for i, data in enumerate(trainloader, 0):

        inputs, targets = data[0].to(device), data[1].to(device)
        optimizer.zero_grad()
        outputs = network(inputs)
        loss = loss_function(outputs, targets)
        loss.backward()
        optimizer.step()
        current_loss += loss.item()
        if i % 10== 9:
            #print('Loss after mini-batch %5d: %.3f' %
            #      (i + 1, current_loss / 100))
            print('Loss after mini-batch ' + str(i+1) + ': ' + str(current_loss/100.0))
            current_loss = 0.0
      if epoch % 5 == 4:
        save_path = './model-fold-' + str(fold) + '-' + str(epoch) + '.pth'
        torch.save(network.state_dict(), save_path)


    print('Training process has finished. Saving trained model.')
    print('Starting testing')

    save_path = f'./model-fold-{fold}.pth'
    torch.save(network.state_dict(), save_path)

    correct, total = 0, 0
    with torch.no_grad():

      for i, data in enumerate(testloader, 0):

        inputs, targets = data[0].to(device), data[1].to(device)
        outputs = network(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()
        #if i % 10 == 9:
        #    print('Accuracy after mini-batch %5d: %.3f' %
        #          (i + 1, 100.0*(correct / total)))

      #print('Accuracy for fold %d: %d %%' % (fold, 100.0 * correct / total))
      print('Accuracy for fold ' + str(fold) + ': ' + str(100.0*correct/total))
      print('--------------------------------')
      results[fold] = 100.0 * (correct / total)

#print(f'K-FOLD CROSS VALIDATION RESULTS FOR {k_folds} FOLDS')
print('K-FOLD CROSS VALIDATION RESULTS FOR ' + str(k_folds) + ' FOLDS')
print('--------------------------------')
sum = 0.0
for key, value in results.items():
    #print(f'Fold {key}: {value} %')
    print('Fold ' + str(key) + ': ' + str(value) + '%')
    sum += value
#print(f'Average: {sum/len(results.items())} %')
print('Average: ' + str(sum/len(results.items())) + '%')


