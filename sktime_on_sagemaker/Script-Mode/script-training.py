import argparse, os
import subprocess, sys
import joblib
import pandas as pd
import numpy as np

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def model_fn(model_dir):
    # pip install sktime
    install('sktime')
    import sktime
    print('*** sktime imported successfully ***')

    from sktime.forecasting.naive import NaiveForecaster
    from sktime.forecasting.model_selection import temporal_train_test_split
    from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
    
    model = joblib.load(os.path.join(model_dir, 'model.joblib'))
    return model


def main():
    # pip install sktime
    install('sktime')
    import sktime
    print('*** sktime imported successfully ***')

    from sktime.forecasting.naive import NaiveForecaster
    from sktime.forecasting.model_selection import temporal_train_test_split
    from sktime.performance_metrics.forecasting import mean_absolute_percentage_error

    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--training', type=str, default=os.environ['SM_CHANNEL_TRAINING'])
    # parser.add_argument('--model-dir', type=str, default='')
    # parser.add_argument('--training', type=str, default='')

    args, _ = parser.parse_known_args()
    model_dir = args.model_dir
    training_dir = args.training

    # Load Data
    filename = os.path.join(training_dir, 'airline.csv')
    temp = pd.read_csv(filename)
    y = pd.Series(temp['Number of airline passengers'].values,
                  index=pd.PeriodIndex(temp['Period'].values, freq='M'))

    y_train, y_test = temporal_train_test_split(y, test_size=36)
    fh = np.arange(1, len(y_test) + 1)  # we add 1 because the `stop` value is exclusive in `np.arange`

    forecaster = NaiveForecaster(strategy="last", sp=12)
    forecaster.fit(y_train)
    y_pred = forecaster.predict(fh)
    print(f'*** sMAPE Loss : {mean_absolute_percentage_error(y_pred, y_test)} ***')

    # Save the model
    model = os.path.join(model_dir, 'model.joblib')
    joblib.dump(forecaster, model)
    print(f'*** Model has been saved in {model} ***')


if __name__ == '__main__':
    main()
