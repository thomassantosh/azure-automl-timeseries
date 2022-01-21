from azureml.automl.core.shared import constants
from azureml.automl.runtime.shared.score import scoring
import matplotlib.pyplot as plt
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    forecast_df = pd.read_csv('prediction.csv', parse_dates=['Date'])
    target_column = 'Load'

    # use automl metrics module
    scores = scoring.score_regression(
        y_test=forecast_df[target_column],
        y_pred=forecast_df['predicted'],
        metrics=list(constants.Metric.SCALAR_REGRESSION_SET))

    # Log metric results
    for key, value in scores.items():
        logging.info(f' Metric: {key}, Metric value:{value:.3f}')

    # Plot outputs
    test_pred = plt.scatter(forecast_df[target_column], forecast_df['predicted'], color='b')
    test_test = plt.scatter(forecast_df[target_column], forecast_df[target_column], color='g')
    plt.legend((test_pred, test_test), ('prediction', 'truth'), loc='upper left', fontsize=8)
    plt.savefig('./imgs/final_result.png')
    #plt.show()

if __name__ == "__main__":
    main()
