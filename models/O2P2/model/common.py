import torch
import torch.nn as nn


class ConvLayer(torch.nn.Module):
    """ Conv Layer Class
    """

    def __init__(self, cin, cout, kernel_size=3, stride=1, padding=0, bn=False, dropout=0):
        super(ConvLayer, self).__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding)
        # TODO: weight initialization? nn.init.xavier_uniform(self.conv.weight)
        self.activation = nn.ReLU()
        self.bn = nn.BatchNorm2d(cout)
        self.dropout = nn.Dropout2d(dropout)

        if bn:
            self.net = nn.Sequential(self.conv, self.dropout, self.bn, self.activation)
        else:
            self.net = nn.Sequential(self.conv, self.dropout, self.activation)

    def output_size(self, input_size):
        return int((input_size + 2*self.padding - self.kernel_size) / self.stride) + 1

    def forward(self, input):
        output = self.net(input)
        return output


class DeConvLayer(torch.nn.Module):
    """ DeConv Layer Class
    """

    def __init__(self, cin, cout, kernel_size=3, stride=1, padding=0, out_padding=0, bn=False, dropout=0):
        super(DeConvLayer, self).__init__()
        self.kernel_size = kernel_size
        self.op = out_padding
        self.stride = stride
        self.padding = padding
        self.deconv = nn.ConvTranspose2d(cin, cout, kernel_size, stride, padding, self.op)
        # TODO: weight initialization? nn.init.xavier_uniform(self.conv.weight)
        self.activation = nn.ReLU()
        self.bn = nn.BatchNorm2d(cout)
        self.dropout = nn.Dropout2d(dropout)

        if bn:
            self.net = nn.Sequential(self.deconv, self.dropout, self.bn, self.activation)
        else:
            self.net = nn.Sequential(self.deconv, self.dropout, self.activation)

    def output_size(self, input_size):
        return (input_size - 1)*self.stride - 2*self.padding + self.kernel_size + self.op

    def forward(self, input):
        output = self.net(input)
        return output


class FullyConnectedLayer(torch.nn.Module):
    """ Fully Connected Layer Class
    """

    def __init__(self, in_size, out_size, dropout=0, act=True):
        super(FullyConnectedLayer, self).__init__()
        self.linear = nn.Linear(in_size, out_size)
        nn.init.xavier_uniform_(self.linear.weight)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.ReLU()

        if act:
            self.net = nn.Sequential(self.linear, self.activation, self.dropout)
        else:
            self.net = nn.Sequential(self.linear, self.dropout)

    def forward(self, input):
        output = self.net(input)
        return output
