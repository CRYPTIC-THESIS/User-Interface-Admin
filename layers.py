import numpy as np
import pandas as pd
from random import uniform

class progress:
    def progress(count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        print('[%s] %s%s ...%s\r' % (bar, percents, '%', status))

class ReLU:
    def __init__(self):
        self.layer_name = "Activation Layer"

    def forward(X):
        out = np.maximum(X, 0)
        cache = X
        return out, cache

    def backward(dout, cache):
        dX = dout.copy()
        dX[cache <= 0] = 0
        return dX

class Dropout:
    def __init__(self):
        self.layer_name = "Dropout Layer"

    def forward(X, p_dropout):
        u = np.random.binomial(1, p_dropout, size=X.shape) / p_dropout
        out = X * u
        cache = u
        return out, cache


    def backward(dout, cache):
        dX = dout * cache
        return dX

class Batch_norm:
    def __init__(self):
        self.layer_name = 'Batch Normalization Layer'
        self.param = {'mode':'','running_mean': 0,'running_var': 0}
        self.gamma = 1
        self.beta = 0

    def forward(x, gamma, beta,param):
        mode = param['mode']
        eps = param.get('eps', 1e-5)
        momentum = param.get('momentum', 0.9)

        N, D = x.shape
        running_mean = param.get('running_mean', np.zeros(D, dtype=x.dtype))
        running_var = param.get('running_var', np.zeros(D, dtype=x.dtype))

        if mode == 'train':
            sample_mean = x.mean(axis=0)
            sample_var = x.var(axis=0)
            
            running_mean = momentum * running_mean + (1 - momentum) * sample_mean
            running_var = momentum * running_var + (1 - momentum) * sample_var
            
            std = np.sqrt(sample_var + eps)
            x_centered = x - sample_mean
            x_norm = x_centered / std
            out = gamma * x_norm + beta
            
            cache = (x_norm, x_centered, std, gamma)
            
        elif mode == 'test':
            x_norm = (x - running_mean) / np.sqrt(running_var + eps)
            out = out = gamma * x_norm + beta
        
        else:
            raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

        # Store the updated running means back into param
        param['running_mean'] = running_mean
        param['running_var'] = running_var

        return out, cache

    def backward(dout, cache):
        
        N = dout.shape[0]
        x_norm, x_centered, std, gamma = cache
        
        dgamma = (dout * x_norm).sum(axis=0)
        dbeta = dout.sum(axis=0)
        
        dx_norm = dout * gamma
        dx = 1/N / std * (N * dx_norm - 
                        dx_norm.sum(axis=0) - 
                        x_norm * (dx_norm * x_norm).sum(axis=0))
        return dx, dgamma, dbeta

class Conv:
    
    def __init__(self, num_filters):
        self.layer_name = 'Convolution 2D Layer'
        self.num_filters = num_filters
        
        #why divide by 9...Xavier initialization
        self.filters = np.random.randn(num_filters, 2, 2)/4
    
    def iterate_regions(self, input):
        #generates all possible 3*3 input regions using valid padding
        
        h,w = input.shape
        
        for i in range(h-2):
            for j in range(w-2):
                in_region = input[i:(i+2), j:(j+2)]
                yield in_region, i, j
                
    def forward(self, input):
        self.last_input = input
        
        h,w = input.shape
        
        output = np.zeros((h-2, w-2, self.num_filters))
        
        for in_regions, i, j in self.iterate_regions(input):
            output[i, j] = np.sum(in_regions * self.filters, axis=(1,2))
        print('Conv Block:',output.shape)
        return output
    
    def backward(self, d_l_d_out, learn_rate):
        '''
        Performs a backward pass of the conv layer.
        - d_L_d_out is the loss gradient for this layer's outputs.
        - learn_rate is a float.
        '''
        d_l_d_filters = np.zeros(self.filters.shape)

        for in_region, i, j in self.iterate_regions(self.last_input):
            for f in range(self.num_filters):
                d_l_d_filters[f] += d_l_d_out[i,j,f] * in_region

        #update filters
        self.filters -= learn_rate * d_l_d_filters

        return None

class maxpool:
    def __init__(self):
        self.layer_name = 'Maxpooling 2D Layer'

    def forward(input, f=2, s=2):
        #Downsample input `input` using a kernel size of `f` and a stride of `s`
        n_c, h_prev, w_prev = input.shape
        
        # calculate output dimensions after the maxpooling operation.
        h = int((h_prev - f)/s)+1 
        w = int((w_prev - f)/s)+1
        
        # create a matrix to hold the values of the maxpooling operation.
        downsampled = np.zeros((n_c, h, w)) 
        
        # slide the window over every part of the input using stride s. Take the maximum value at each step.
        for i in range(n_c):
            curr_y = out_y = 0
            # slide the max pooling window vertically across the input
            while curr_y + f <= h_prev:
                curr_x = out_x = 0
                # slide the max pooling window horizontally across the input
                while curr_x + f <= w_prev:
                    # choose the maximum value within  the window at each step and store it to the output matrix
                    downsampled[i, out_y, out_x] = np.max(input[i, curr_y:curr_y+f, curr_x:curr_x+f])
                    curr_x += s
                    out_x += 1
                curr_y += s
                out_y += 1
        downsampled = downsampled.reshape(downsampled.shape[0], (downsampled.shape[1]*downsampled.shape[2]))
        print('Maxpooling Layer:',downsampled.shape)
        return downsampled

class LSTM:
    def __init__(self, value_to_idx, idx_to_value, vocab_size, n_h=100, seq_len=25,
                 epochs=10, lr=0.001, beta1=0.9, beta2=0.999):
        """
        Implementation of simple character-level LSTM using Numpy
        """
        self.layer_name = 'LSTM Layer'
        self.value_to_idx = value_to_idx  # characters to indices mapping
        self.idx_to_value = idx_to_value  # indices to characters mapping
        self.vocab_size = vocab_size  # no. of unique characters in the training data
        self.n_h = n_h  # no. of units in the hidden layer
        self.seq_len = seq_len  # no. of time steps, also size of mini batch
        self.epochs = epochs  # no. of training iterations
        self.lr = lr  # learning rate
        self.beta1 = beta1  # 1st momentum parameter
        self.beta2 = beta2  # 2nd momentum parameter

        # -----initialise weights and biases-----#
        self.params = {}
        std = (1.0 / np.sqrt(self.vocab_size + self.n_h))  # Xavier initialisation

        # forget gate
        self.params["Wf"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bf"] = np.ones((self.n_h, 1))

        # input gate
        self.params["Wi"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bi"] = np.zeros((self.n_h, 1))

        # cell gate
        self.params["Wc"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bc"] = np.zeros((self.n_h, 1))

        # output gate
        self.params["Wo"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bo"] = np.zeros((self.n_h, 1))

        # output
        self.params["Wv"] = np.random.randn(self.vocab_size, self.n_h) * \
                            (1.0 / np.sqrt(self.vocab_size))
        self.params["bv"] = np.zeros((self.vocab_size, 1))

        # -----initialise gradients and Adam parameters-----#
        self.grads = {}
        self.adam_params = {}

        for key in self.params:
            self.grads["d" + key] = np.zeros_like(self.params[key])
            self.adam_params["m" + key] = np.zeros_like(self.params[key])
            self.adam_params["v" + key] = np.zeros_like(self.params[key])

        self.smooth_loss = -np.log(1.0 / self.vocab_size) * self.seq_len
        return

    def sigmoid(self, x):
        """
        Smoothes out values in the range of [0,1]
        """
        return 1 / (1 + np.exp(-x))

    def softmax(self, x):
        """
        Normalizes output into a probability distribution
        """
        e_x = np.exp(x - np.max(x))  # max(x) subtracted for numerical stability
        return e_x / np.sum(e_x)

    def clip_grads(self):
        """
        Limits the magnitude of gradients to avoid exploding gradients
        """
        for key in self.grads:
            np.clip(self.grads[key], -5, 5, out=self.grads[key])
        return

    def reset_grads(self):
        """
        Resets gradients to zero before each backpropagation
        """
        for key in self.grads:
            self.grads[key].fill(0)
        return

    def update_params(self, batch_num):
        """
        Updates parameters with Adam
        """
        for key in self.params:
            self.adam_params["m" + key] = self.adam_params["m" + key] * self.beta1 + \
                                          (1 - self.beta1) * self.grads["d" + key]
            self.adam_params["v" + key] = self.adam_params["v" + key] * self.beta2 + \
                                          (1 - self.beta2) * self.grads["d" + key] ** 2

            m_correlated = self.adam_params["m" + key] / (1 - self.beta1 ** batch_num)
            v_correlated = self.adam_params["v" + key] / (1 - self.beta2 ** batch_num)
            self.params[key] -= self.lr * m_correlated / (np.sqrt(v_correlated) + 1e-8)
        return

    def sample(self, h_prev, c_prev, sample_size):
        """
        Outputs a sample sequence from the model
        """
        x = np.zeros((self.vocab_size, 1))
        h = h_prev
        c = c_prev
        sample_string = ""

        for t in range(sample_size):
            y_hat, _, h, _, c, _, _, _, _ = self.forward_step(x, h, c)

            # get a random index within the probability distribution of y_hat(ravel())
            idx = np.random.choice(range(self.vocab_size), p=y_hat.ravel())
            x = np.zeros((self.vocab_size, 1))
            x[idx] = 1

            # find the char with the sampled index and concat to the output string
            char = self.idx_to_char[idx]
            sample_string += str(char) + "-->"
        return sample_string

    def forward_step(self, x, h_prev, c_prev):
        """
        Implements the forward propagation for one time step
        """
        z = np.row_stack((h_prev, x))

        f = self.sigmoid(np.dot(self.params["Wf"], z) + self.params["bf"])
        i = self.sigmoid(np.dot(self.params["Wi"], z) + self.params["bi"])
        c_bar = np.tanh(np.dot(self.params["Wc"], z) + self.params["bc"])

        c = f * c_prev + i * c_bar
        o = self.sigmoid(np.dot(self.params["Wo"], z) + self.params["bo"])
        h = o * np.tanh(c)

        v = np.dot(self.params["Wv"], h) + self.params["bv"]
        y_hat = self.softmax(v)
        return y_hat, v, h, o, c, c_bar, i, f, z

    def backward_step(self, y, y_hat, dh_next, dc_next, c_prev, z, f, i, c_bar, c, o, h):
        """
        Implements the backward propagation for one time step
        """
        dv = np.copy(y_hat)
        dv[y] -= 1  # yhat - y

        self.grads["dWv"] += np.dot(dv, h.T)
        self.grads["dbv"] += dv

        dh = np.dot(self.params["Wv"].T, dv)
        dh += dh_next

        do = dh * np.tanh(c)
        da_o = do * o * (1 - o)
        self.grads["dWo"] += np.dot(da_o, z.T)
        self.grads["dbo"] += da_o

        dc = dh * o * (1 - np.tanh(c) ** 2)
        dc += dc_next

        dc_bar = dc * i
        da_c = dc_bar * (1 - c_bar ** 2)
        self.grads["dWc"] += np.dot(da_c, z.T)
        self.grads["dbc"] += da_c

        di = dc * c_bar
        da_i = di * i * (1 - i)
        self.grads["dWi"] += np.dot(da_i, z.T)
        self.grads["dbi"] += da_i

        df = dc * c_prev
        da_f = df * f * (1 - f)
        self.grads["dWf"] += np.dot(da_f, z.T)
        self.grads["dbf"] += da_f

        dz = (np.dot(self.params["Wf"].T, da_f)
              + np.dot(self.params["Wi"].T, da_i)
              + np.dot(self.params["Wc"].T, da_c)
              + np.dot(self.params["Wo"].T, da_o))

        dh_prev = dz[:self.n_h, :]
        dc_prev = f * dc
        return dh_prev, dc_prev

    def forward_backward(self, x_batch, y_batch, h_prev, c_prev):
        """
        Implements the forward and backward propagation for one batch
        """
        x, z = {}, {}
        f, i, c_bar, c, o = {}, {}, {}, {}, {}
        y_hat, v, h = {}, {}, {}

        # Values at t= - 1
        h[-1] = h_prev
        c[-1] = c_prev

        loss = 0
        for t in range(self.seq_len):
            x[t] = np.zeros((self.vocab_size, 1))
            x[t][x_batch[t]] = 1

            y_hat[t], v[t], h[t], o[t], c[t], c_bar[t], i[t], f[t], z[t] = \
                self.forward_step(x[t], h[t - 1], c[t - 1])

            loss += -np.log(y_hat[t][y_batch[t], 0])

        self.reset_grads()

        dh_next = np.zeros_like(h[0])
        dc_next = np.zeros_like(c[0])

        for t in reversed(range(self.seq_len)):
            dh_next, dc_next = self.backward_step(y_batch[t], y_hat[t], dh_next,
                                                  dc_next, c[t - 1], z[t], f[t], i[t],
                                                  c_bar[t], c[t], o[t], h[t])
        return loss, h[self.seq_len - 1], c[self.seq_len - 1]

    def gradient_check(self, x, y, h_prev, c_prev, num_checks=10, delta=1e-6):
        """
        Checks the magnitude of gradients against expected approximate values
        """
        #print("**********************************")
        print("Gradient check...\n")

        _, _, _ = self.forward_backward(x, y, h_prev, c_prev)
        grads_numerical = self.grads

        for key in self.params:
            #print("---------", key, "---------")
            test = True

            dims = self.params[key].shape
            grad_numerical = 0
            grad_analytical = 0

            for _ in range(num_checks):  # sample 10 neurons

                idx = int(uniform(0, self.params[key].size))
                old_val = self.params[key].flat[idx]

                self.params[key].flat[idx] = old_val + delta
                J_plus, _, _ = self.forward_backward(x, y, h_prev, c_prev)

                self.params[key].flat[idx] = old_val - delta
                J_minus, _, _ = self.forward_backward(x, y, h_prev, c_prev)

                self.params[key].flat[idx] = old_val

                grad_numerical += (J_plus - J_minus) / (2 * delta)
                grad_analytical += grads_numerical["d" + key].flat[idx]

            grad_numerical /= num_checks
            grad_analytical /= num_checks

            rel_error = abs(grad_analytical - grad_numerical) / abs(grad_analytical + grad_numerical)

            if rel_error > 1e-2:
                if not (grad_analytical < 1e-6 and grad_numerical < 1e-6):
                    test = False
                    assert (test)

            #print('Approximate: \t%e, Exact: \t%e =>  Error: \t%e' % (grad_numerical, grad_analytical, rel_error))
        print("\nTest successful!")