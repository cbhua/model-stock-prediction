import torch
import configparser
import numpy as np
import matplotlib.pyplot as plt

from torch.utils.data import DataLoader 
from src.models.lstm import LSTM_model
from src.models.gru import GRU_model
from src.utils.dataset import SampleDataset


config = configparser.ConfigParser()
config.read('config.ini')
config_use = config['switcher']['config_use']

test_set = SampleDataset(config[config_use]['save_dataset_path'] + 
                          config[config_use]['src_dataset_path'].split('/')[-1][:-4] + 
                          '_test.npy'
                        )
test_loader = DataLoader(
                          dataset = test_set, 
                          batch_size = int(config[config_use]['test_batch_size']), 
                          shuffle = False
                         )

if config[config_use]['module'] == 'gru':
    model = GRU_model(
        num_classes = int(config[config_use]['num_classes']),
        input_size = int(config[config_use]['input_size']),
        hidden_size = int(config[config_use]['hidden_size']),
        num_layers = int(config[config_use]['num_layers']),
        seq_length = int(config[config_use]['seq_length'])
    )
else:
    model = LSTM_model(
        num_classes = int(config[config_use]['num_classes']),
        input_size = int(config[config_use]['input_size']),
        hidden_size = int(config[config_use]['hidden_size']),
        num_layers = int(config[config_use]['num_layers']),
        seq_length = int(config[config_use]['seq_length'])
    )
model.load_state_dict(torch.load(config[config_use]['save_model_path']))
model.eval()

loss_list = []
loss_fuction = torch.nn.MSELoss()

for index, data in enumerate(test_loader):
    input = data[:, np.newaxis, :-1].float()
    target = data[:, -1:].float()
    output = model(input)

    loss = loss_fuction(output, target)
    loss_list.append(loss)

print(loss_list)
