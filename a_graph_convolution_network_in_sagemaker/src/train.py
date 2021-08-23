#!/usr/bin/env python

import os, json
import pickle

import torch as th
import torch.nn.functional as F 

from dgl.data import CoraFullDataset
from dgl.data.utils import split_dataset, save_graphs, load_graphs

from model import GraphConvolutionalNetwork


def main():
    # setup variables
    config_dir = '/opt/ml/input/config'
    model_dir = '/opt/ml/model'

    with open(os.path.join(config_dir, 'hyperparameters.json'), 'r') as file:
        parameters_dict = json.load(file)

        learning_rate = float(parameters_dict['learning-rate'])
        epochs = int(parameters_dict['epochs'])

    # loading graph model
    glist, label_dict = load_graphs(os.path.join(model_dir, 'dgl-citation-network-graph.bin'))
    graph = glist[0]
    features = graph.ndata['feat']
    labels = graph.ndata['label']
    number_of_labels = len(labels.unique())

    # loading train/test spilit indices
    with open(os.path.join(model_dir, '/train_indices.bin'), 'rb') as train_file:
        train_mask = pickle.load(train_file)
    
    with open(os.path.join(model_dir, '/validation_indices.bin'), 'rb') as validation_file:
        val_mask = pickle.load(validation_file)

    # creating model
    model = GraphConvolutionalNetwork(features.shape[1], 16, number_of_labels)
    optimizer = th.optim.Adam(model.parameters(), lr=learning_rate)

    # training
    for epoch in range(epochs):
        pred = model(graph, features)
        loss = F.cross_entropy(pred[train_mask], labels[train_mask].to(th.long))

        train_acc = (labels[train_mask] == pred[train_mask].argmax(1)).float().mean()
        val_acc = (labels[val_mask] == pred[val_mask].argmax(1)).float().mean()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'Epoch {epoch}/{epochs} | Loss: {loss.item()}, train_accuracy: {train_acc}, val_accuracy: {val_acc}')


    # saving model
    th.save(model, os.path.join(model_dir, 'dgl-citation-network-model.pt'))

if __name__ == '__main__':
    main()