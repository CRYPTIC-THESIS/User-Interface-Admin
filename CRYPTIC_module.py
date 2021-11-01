import numpy as np
import layers as layer
import data_prep as dp
import pandas as pd

def format_LSTM(data):
    
    vals = set(data)
    vals_size = len(vals)

    vals_to_idx = {w: i for i,w in enumerate(vals)}
    idx_to_vals = {i: w for i,w in enumerate(vals)}

    return vals_to_idx,idx_to_vals,vals,vals_size

def network_archi(network):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\t\tCRYPTIC Network")
    for i in network:
        print('|\t'+i.layer_name+'\t|')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def LSTM_pass(lstm,X,epoch,verbose,X_trimmed,J):
            
    h_prev = np.zeros((lstm.n_h, 1))
    c_prev = np.zeros((lstm.n_h, 1))

    for j in range(0, len(X_trimmed) - lstm.seq_len, lstm.seq_len):
        # prepare batches
        x_batch = [lstm.vals_to_idx[ch] for ch in X_trimmed[j: j + lstm.seq_len]]
        y_batch = [lstm.vals_to_idx[ch] for ch in X_trimmed[j + 1: j + lstm.seq_len + 1]]

        loss, h_prev, c_prev = lstm.forward_backward(x_batch, y_batch, h_prev, c_prev)

        # smooth out loss and store in list
        lstm.smooth_loss = lstm.smooth_loss * 0.999 + loss * 0.001
        J.append(lstm.smooth_loss)

        # check gradients
        if epoch == 0 and j == 0:
            lstm.gradient_check(x_batch, y_batch, h_prev, c_prev, num_checks=10, delta=1e-7)

        lstm.clip_grads()

        batch_num = epoch * lstm.epochs + j / lstm.seq_len + 1
        lstm.update_params(batch_num)

        # print out loss and sample string
        if verbose:
            if j % 400000 == 0:
                print('Epoch:', epoch, '\tBatch:', j, "-", j + lstm.seq_len,'\tLoss:', round(lstm.smooth_loss, 2))

    return J,h_prev, c_prev

def train(epochs,data,X):
    print('CRYPTIC NETWORK TRAINING\n\n')
    con = layer.Conv(5)
    con1 = layer.Conv(3)
    vals_to_idx,idx_to_vals,vals,vals_size = format_LSTM(X)
    lstm = layer.LSTM(vals_to_idx, idx_to_vals, vals_size, epochs, lr = 0.01)
    J = []  # to store losses
    verbose = True
    num_batches = len(X) // lstm.seq_len
    out = con.forward(data)
    out = layer.maxpool(out)
    out = con1.forward(out)
    out = layer.maxpool(out)
    X_trimmed = X[: num_batches * lstm.seq_len]  # trim input to have full sequences
    for epoch in range(epochs):
        '''
        out = con.forward(data)
        out = layer.maxpool(out)
        out = con1.forward(out)
        out = layer.maxpool(out)
        '''
        J,h,c = LSTM_pass(lstm,out.flatten(),epoch,verbose,X_trimmed,J)


        trained_network = [con,con1,lstm,h,c]

    return J,trained_network


def predict_crypto(network,input):
    #predict cryptocurrency up to 14 days

    #Initialize Model
    for i  in range(14):
        out = network[0].forward(input)
        out = layer.maxpool(out)
        out = network[1].forward(out)
        out = layer.maxpool(out)
        
        out = network[2].forward_step(out,network[3],network[4])

df = pd.read_csv('/home/jeremy/Downloads/BTC_USD_2014-11-04_2021-11-01-CoinDesk.csv')
dataset = pd.DataFrame(columns = ['Close','Open','High','Low','Open1','High1','Low1'])
Y = np.array(df['Date'])
dataset['Close'] = df['Closing Price (USD)']
dataset['Open'] = df['24h Open (USD)']
dataset['High'] = df['24h High (USD)']
dataset['Low'] = df['24h Low (USD)']
dataset['Open1'] = df['24h Open (USD)']
dataset['High1'] = df['24h High (USD)']
dataset['Low1'] = df['24h Low (USD)']
X = np.array(dataset['Close'])
dataset = np.array(dataset)

labels = [i for i in range(len(dataset))]
labels = np.array(labels,dtype=int)

train(300,dataset,X)

