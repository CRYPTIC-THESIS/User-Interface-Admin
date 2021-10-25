import numpy as np
import layers as l
import data_prep as dp

def train(network, epochs,data):
    for epoch in range(epochs):
        output = data
        for layer in network:
            output = layer.forward(output)
            #NOT DONE

def network_archi(network):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|\t\tCRYPTIC Network\t\t\t|\n|\t\t\t\t\t\t|")
    for i in network:
        print('|\t'+i.layer_name+'\t|')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
bar = l.progress
epochs = 300
value_to_idx,idx_to_value,seq_size = dp.init_lstm()
network = [ l.Conv(16),
            l.maxpool(),
            l.Conv(8),
            l.maxpool(),
            l.LSTM(value_to_idx,idx_to_value,seq_size),
            l.Dropout(),
            l.ReLU(),
            l.Batch_norm(),
            l.Dropout(),
            l.ReLU(),
            l.Batch_norm()]
#Print the network architecture
network_archi(network)




