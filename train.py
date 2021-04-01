import torch
import configparser
import numpy as np

from torch.utils.data import DataLoader 
from src.models.lstm import LSTM_model
from src.utils.dataset import SampleDataset
from src.utils.data_transfer import data_transfer


config = configparser.ConfigParser()
config.read('config.ini')
config_use = config['switcher']['config_use']

# Step 1. Transfer csv to numpy.array
data_transfer(config[config_use]['src_dataset_path'], 
              config[config_use]['save_dataset_path'], 
              float(config[config_use]['train_dataset_rate'])
             )

# Step 2. Create datasets
train_set = SampleDataset(config[config_use]['save_dataset_path'] + 
                          config[config_use]['src_dataset_path'].split('/')[-1][:-4] + 
                          '_train.npy'
                         )

# Step 3. Create dataloader
train_loader = DataLoader(
                          dataset = train_set, 
                          batch_size = int(config[config_use]['batch_size']), 
                          shuffle = False
                         )

# Step 4. Init model
model = LSTM_model(
    num_classes = int(config[config_use]['num_classes']),
    input_size = int(config[config_use]['input_size']),
    hidden_size = int(config[config_use]['hidden_size']),
    num_layers = int(config[config_use]['num_layers']),
    seq_length = int(config[config_use]['seq_length'])
)

# Step 5. Init utils
loss_list = []
loss_fuction = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = float(config[config_use]['learning_rate']))

# Step 6. Train
for epoch in range(int(config[config_use]['epoches'])):
    for index, data in enumerate(train_loader):
        input = data[:, np.newaxis, :-1]
        output = model(input)

        optimizer.zero_grad()
        loss = loss_fuction(output, data[:, -1])
        loss.backward()
        loss_list.append(loss)
    if epoch % 100 == 0:
        print('Epoch: {}, Loss: {:1.4f}'.format(epoch, loss_list[-1]))

# Step 7. Save model
torch.save(model.state_dict(), config[config_use]['save_model_path'])