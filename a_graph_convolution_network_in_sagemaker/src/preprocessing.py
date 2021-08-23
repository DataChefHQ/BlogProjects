#!/user/bin/env python

from __future__ import with_statement
import os
import pickle
from typing import Any
from dgl.data import CoraFullDataset
from dgl.data.utils import save_graphs, split_dataset


config_dir = '/opt/ml/input/config'
model_dir = '/opt/ml/model'


def main():
    # downloading dataset
    dataset = CoraFullDataset()
    graph = dataset[0]

    # saving graph
    save_graphs(os.path.join(model_dir, 'dgl-citation-network-graph.bin'), graph)

    # saving train/val indices
    train_mask, val_mask = split_dataset(graph, [0.8, 0.2])

    with open(os.path.join(model_dir, '/train_indices.bin'), 'wb') as train_file:
        pickle.dump(train_mask.indices, train_file)
    
    with open(os.path.join(model_dir, '/validation_indices.bin'), 'wb') as validation_file:
        pickle.dump(val_mask.indices, validation_file)


if __name__ == '__main__':
    main()