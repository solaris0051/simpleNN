import numpy as np
import matplotlib.pyplot as plt

# -- input data and correct data --
input_data = np.linspace(-np.pi, np.pi)  # original input dataset
correct_data = np.sin(input_data)        # correct dataset
input_data = input_data/np.pi            # to range the realm from -1.0 to 1.0
n_data = len(correct_data)               # number of data

# -- config --
n_in = 1   # the number of neurons at the input layer
n_mid = 12 # the number of neurons at the middle layers
n_out = 1  # the number of neurons at the output layer

wb_width = 0.28  # width of weight and bias
eta = 0.15       # learning coefficient
epoch = 1001
interval = 50    # monitoring interval

# -- supercalss --
class BaseLayer:
    def __init__(self, n_upper, n):
        self.w = wb_width * np.random.randn(n_upper, n)  # weight matrix
        self.b = wb_width * np.random.randn(n)  # bias vector

    def update(self, eta):
        self.w -= eta * self.grad_w
        self.b -= eta * self.grad_b

# -- middlelayer--
class MiddleLayer(BaseLayer):
    def forward(self, x):  # foreward-propagation
        self.x = x
        u = np.dot(x, self.w) + self.b
        self.y = 1/(1+np.exp(-u))  # sigmoid function

    def backward(self, grad_y):  # back-propagation
        delta = grad_y * (1-self.y)*self.y  # differential calculus of sigmoid function

        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis=0)

        self.grad_x = np.dot(delta, self.w.T)


# -- output layer --
class OutputLayer(BaseLayer):
    def forward(self, x):  # foreward-propagation
        self.x = x
        u = np.dot(x, self.w) + self.b
        self.y = u  # identity function

    def backward(self, t):  # back-propagation
        delta = self.y - t

        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis=0)

        self.grad_x = np.dot(delta, self.w.T)


# -- initializing each layer --
middle_layer1 = MiddleLayer(n_in, n_mid)
middle_layer2 = MiddleLayer(n_mid, n_mid)
output_layer = OutputLayer(n_mid, n_out)

# -- start learning --
for i in range(epoch):

    # shffle index
    index_random = np.arange(n_data)
    np.random.shuffle(index_random)

    # plot the results
    total_error = 0
    plot_x = []
    plot_y = []

    for idx in index_random:

        x = input_data[idx]  # original input dataset
        t = correct_data[idx]  # correct dataset

        # foreward-propagation
        middle_layer1.forward(np.array([[x]]))  # transform input data to middle layer1 to matrix
        middle_layer2.forward(middle_layer1.y)
        output_layer.forward(middle_layer2.y)

        # back-propagation
        output_layer.backward(np.array([[t]]))  # express correct dataset as matrix
        middle_layer2.backward(output_layer.grad_x)
        middle_layer1.backward(middle_layer2.grad_x)


        # update wight and bias
        middle_layer1.update(eta)
        middle_layer2.update(eta)
        output_layer.update(eta)

        if i%interval == 0:

            y = output_layer.y[0][0]  # get numbers from matrix

            # error assessment
            total_error += 1.0/2.0*np.sum(np.square(y - t))  # mean square error

            # append outputs
            plot_x.append(x)
            plot_y.append(y)

    if i%interval == 0:

        # plot outpus
        plt.plot(input_data, correct_data, linestyle="dashed")
        plt.scatter(plot_x, plot_y, marker="+")
        plt.show()

        # print epoch number and errors
        print("Epoch:" + str(i) + "/" + str(epoch), "Error:" + str(total_error/n_data))
