#!/usr/bin/env python

# geting node indeces and return predicted labels

import os
from dgl.convert import graph 
import pandas as pd 
from io import StringIO

from dgl.data.utils import load_graphs
import torch as th

import flask
from flask import Flask, Response


model_dir = '/opt/ml/model'
graph_dir = '/opt/ml/input/data'

glist, label_dict = load_graphs(os.path.join(model_dir, 'dgl-citation-network-graph.bin'))
graph = glist[0]
model = th.load(os.path.join(model_dir, 'dgl-citation-network-model.pt'))
features = graph.ndata['feat']
pred = model(graph, features)

app = Flask(__name__)

@app.route("/ping", methods=["GET"]) 
def ping():
    return Response(response="\n", status=200)

@app.route("/invocations", methods=["POST"]) 
def predict():
    if flask.request.content_type == 'text/csv': 
        data = flask.request.data.decode('utf-8') 
        s = StringIO(data)
        data = pd.read_csv(s, header=None) 
        response = pred[data.values]
        response = str(response)
    else:
        return flask.Response(response='CSV data only', status=415, mimetype='text/plain')

    return Response(response=response, status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)