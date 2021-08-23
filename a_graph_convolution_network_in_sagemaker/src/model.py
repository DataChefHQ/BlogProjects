import torch as th
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn import GraphConv


class GraphConvolutionalNetwork(nn.Module):
    def __init__(self, in_feat, h_feat, out_feat):
        super().__init__()

        self.gcl1 = GraphConv(in_feat, h_feat)
        self.relu = nn.ReLU()
        self.gcl2 = GraphConv(h_feat, out_feat)

    def forward(self, graph, in_feat):
        x = self.gcl1(graph, in_feat)
        x = self.relu(x)
        x = self.gcl2(graph, x)

        return x
