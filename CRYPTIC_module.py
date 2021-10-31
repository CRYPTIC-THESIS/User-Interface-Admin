import numpy as np
import layers as layer
import data_prep as dp

def format_LSTM(data):
    for x in range(len(data)):
        if((x+3) > len(data)) or x == len(data)-3:
            break
        if(x==0):
            X = [np.array(data[x:x+3])]
            Y = [data[x+3]]
        else:    
            X = np.append(X,[np.array(data[x:x+3])],axis=0)
            Y = np.append(Y,data[x+3])
    
    vals = set(data)
    vals_size = len(vals)

    vals_to_idx = {w: i for i,w in enumerate(vals)}
    idx_to_vals = {i: w for i,w in enumerate(vals)}

    print("Dataset Created")

    return X,Y,vals_to_idx,idx_to_vals,vals,vals_size

def train(epochs,data,verbose=True):
    
    for epoch in range(epochs):
        output = data

        con = layer.Conv(5)
        con1 = layer.Conv(2)
        
        out = con.forward(output)
        out = layer.maxpool(out)
        out = con1.forward(out)
        out = layer.maxpool(out)
            
        J = []  # to store losses

        X,Y,vals_to_idx,idx_to_vals,vals,vals_size = format_LSTM(out)
        lstm = layer.LSTM(vals_to_idx, idx_to_vals, vals_size, epochs, lr = 0.01)
        num_batches = len(X) // layer.seq_len
        X_trimmed = output[: num_batches * layer.seq_len]  # trim input to have full sequences

        
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
                    print('Epoch:', epoch, '\tBatch:', j, "-", j + layer.seq_len,'\tLoss:', round(layer.smooth_loss, 2))

    return J, lstm.params

def predict_crypto():
    #predict cryptocurrency up to 14 days

    #Initialize Model
    for i  in range(14):
        print('Predict Daily')

def network_archi(network):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n|\t\tCRYPTIC Network\t\t\t|\n|\t\t\t\t\t\t|")
    for i in network:
        print('|\t'+i.layer_name+'\t|')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
bar = layer.progress
epochs = 300
value_to_idx,idx_to_value,seq_size = dp.init_lstm()
network = [ layer.Conv(5),
            layer.maxpool(),
            layer.Conv(2),
            layer.maxpool(),
            layer.LSTM(value_to_idx,idx_to_value,seq_size),
            layer.Dropout(),
            layer.ReLU(),
            layer.Batch_norm(),
            layer.Dropout(),
            layer.ReLU(),
            layer.Batch_norm()]
#Print the network architecture
network_archi(network)

