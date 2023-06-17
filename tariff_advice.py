import numpy as np


class TariffAdvisor:
    def __init__(self):
        self.weights1 = 2 * np.random.random((4, 3)) - 1
        self.weights2 = 2 * np.random.random((3, 3)) - 1
        self.weights3 = 2 * np.random.random((3, 3)) - 1
        self.weights4 = 2 * np.random.random((3, 5)) - 1
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def predict(self, inputs):
        #inputs = inputs.astype(float)
        hidden_layer1 = self.sigmoid(np.dot(inputs, self.weights1))
        hidden_layer2 = self.sigmoid(np.dot(hidden_layer1, self.weights2))
        hidden_layer3 = self.sigmoid(np.dot(hidden_layer2, self.weights3))
        output = self.sigmoid(np.dot(hidden_layer3, self.weights4))
        return output
    
    def convertInput(value, old_min, old_max, new_min=-1, new_max=1):
        return (value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

    def train(self, inputs, labels, iterations):
        inputs = inputs.astype(float)
        labels = labels.astype(float)
        
        for i in range(iterations):
            hidden_layer1 = self.sigmoid(np.dot(inputs, self.weights1))
            hidden_layer2 = self.sigmoid(np.dot(hidden_layer1, self.weights2))
            hidden_layer3 = self.sigmoid(np.dot(hidden_layer2, self.weights3))
            output = self.sigmoid(np.dot(hidden_layer3, self.weights4))
            
            error = labels - output
            adjustments = error * self.sigmoid_derivative(output)
            self.weights4 += np.dot(hidden_layer3.T, adjustments)
            
            hidden_error3 = np.dot(adjustments, self.weights4.T)
            hidden_adjustments3 = hidden_error3 * self.sigmoid_derivative(hidden_layer3)
            self.weights3 += np.dot(hidden_layer2.T, hidden_adjustments3)
            
            hidden_error2 = np.dot(hidden_adjustments3, self.weights3.T)
            hidden_adjustments2 = hidden_error2 * self.sigmoid_derivative(hidden_layer2)
            self.weights2 += np.dot(hidden_layer1.T, hidden_adjustments2)
            
            hidden_error1 = np.dot(hidden_adjustments2, self.weights2.T)
            hidden_adjustments1 = hidden_error1 * self.sigmoid_derivative(hidden_layer1)
            self.weights1 += np.dot(inputs.T, hidden_adjustments1)

def load_nn():
    nn = TariffAdvisor()
    
    loaded_data = np.load("weights.npz")
    
    nn.weights1 = loaded_data["w1"]
    nn.weights2 = loaded_data["w2"]
    nn.weights3 = loaded_data["w3"]
    nn.weights4 = loaded_data["w4"]
    
    return nn
    

# tests
# if __name__ == "__main__":
#     nn = TariffAdvisor()
#     inputs = np.array([
#         [3,2,2,3],
#         [2,2,3,1],
#         [2,1,2,1],
#         [3,3,3,3],
#         [1,1,1,1] ]) - 2
#     labels = np.array([
#         [1,0,0,0,0],
#         [0,1,0,0,0],
#         [0,0,1,0,0],
#         [0,0,0,1,0],
#         [0,0,0,0,1] ])
#     nn.train(inputs, labels, 1000)
# 
#     for i, ins in enumerate(inputs):
#         print(f"input: {ins}, out: {np.round(nn.predict(ins), 1)}, error: {nn.predict(ins)-labels[i]}\n")
# 
#     ws = {'w1': array([[-0.59324725,  2.29812294, -1.85393209],
#            [-2.38027967, -0.58776987, -1.70942779],
#            [-2.15780396,  3.07047142, -0.14869593],
#            [-0.50106943, -1.46590069, -1.67490944]]), 'w2': array([[ 3.50920037, -1.85977297, -3.27782463],
#            [-2.840139  ,  4.8287195 ,  2.63938683],
#            [ 4.04562891, -1.16946216, -1.73891269]]), 'w3': array([[-6.62823345,  7.21059035,  4.62214223],
#            [ 3.1958672 , -1.0210842 , -5.61744577],
#            [ 3.05202392, -2.07654738, -3.62941825]]), 'w4': array([[ -0.11482692,  -3.34468087, -10.44340713,   2.40572812,
#              -6.30670041],
#            [ -0.9325851 ,   3.44264845,   3.9792921 ,  -9.49723297,
#              -5.13754521],
#            [ -4.29472885, -12.20782212,  -5.75082529,  -3.94013424,
#               7.51471833]])}
# 
#     # Save the dictionary to a file
#     np.savez('weights.npz', **ws)

