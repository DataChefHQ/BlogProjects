#!/usr/bin/env python

import pandas as pd
import numpy as np
import sktime
print('*** sktime imported successfully ***')
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
import joblib
import os, json

if __name__ == '__main__':
    config_dir = '/opt/ml/input/config'
    training_dir = '/opt/ml/input/data/training'
    model_dir = '/opt/ml/model'
    
    with open(os.path.join(config_dir, 'hyperparameters.json')) as f:
        hp = json.load(f)
        print(hp)
        normalize = hp['normalize']
        test_size = float(hp['test-size'])
        random_state = int(hp['random-state'])

    # Load Data
    filename = os.path.join(training_dir, 'airline.csv')
    temp = pd.read_csv(filename)
    y = pd.Series(temp['Number of airline passengers'].values,
                  index=pd.PeriodIndex(temp['Period'].values, freq='M'))

    y_train, y_test = temporal_train_test_split(y, test_size=36)
    fh = np.arange(1, len(y_test) + 1)
    forecaster = NaiveForecaster(strategy="last", sp=12)
    forecaster.fit(y_train)
    y_pred = forecaster.predict(fh)
    print(f'*** sMAPE Loss : {mean_absolute_percentage_error(y_pred, y_test)} ***')

    # Save the model
    joblib.dump(forecaster, os.path.join(model_dir, 'model.joblib'))
    print('*** Model has been saved ***')
