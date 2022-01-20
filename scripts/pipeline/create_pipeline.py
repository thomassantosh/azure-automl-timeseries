# Create the training pipeline
import sys
import os.path
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
import pandas as pd
import logging
from azureml.core import Run, Dataset
from azureml.core.compute import ComputeTarget
from azureml.train.automl import AutoMLConfig
from azureml.pipeline.steps import AutoMLStep, PythonScriptStep
from azureml.train.automl.run import AutoMLRun
from azureml.core.runconfig import RunConfiguration, DEFAULT_CPU_IMAGE, DockerConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.pipeline.core import Pipeline, PipelineData, TrainingOutput
from azureml.pipeline.core.graph import PipelineParameter
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.core.experiment import Experiment
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def main():

    # Setup run configuration
    docker_config = DockerConfiguration(use_docker=True)
    run_config = RunConfiguration()
    run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE
    run_config.docker = docker_config
    run_config.environment.python.user_managed_dependencies = False
    run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['pandas', 'pip','python-dotenv'])

    # Setup resources
    experiment_name='forecasting_for_energy_prices'
    cpu_cluster = ComputeTarget(workspace=ws, name='cpu-cluster')
    def_blob_store = ws.get_default_datastore()

    # Setup datasets
    dataset_name = 'NYC-trainingset-Dec2020'
    ds = Dataset.get_by_name(workspace=ws, name=dataset_name)
    df = ds.to_pandas_dataframe().reset_index(drop=True)
    logging.info( df.head())
    logging.info( df.tail() )
    logging.info( df.info())

    metrics_data = PipelineData(    
            name='metrics_data',    
            datastore=def_blob_store,    
            pipeline_output_name='metrics_output',    
            training_output=TrainingOutput(type='Metrics')    
            )    
        
    model_data = PipelineData(    
            name='best_model_data',    
            datastore=def_blob_store,    
            pipeline_output_name='model_output',    
            training_output=TrainingOutput(type='Model')    
            )

    # Setup the forecasting parameters
    forecasting_parameters = ForecastingParameters(
        time_column_name='Date',
        forecast_horizon=48,
        target_rolling_window_size=3, # for simple regression, comment this
        feature_lags='auto',# for simple regression, comment this
        target_lags=12,# for simple regression, comment this
        freq='5T',
        validate_parameters=True
    )

    # Featurization
    featurization_config = FeaturizationConfig()
    featurization_config.drop_columns = ['TZ', 'Place', 'Code']
    featurization_config.add_transformer_params('Imputer', ['Load'], {"strategy": "ffill"})

    # Setup the classifier
    label = 'Load'
    automl_settings = {
        "task": 'forecasting',
        "primary_metric":'normalized_root_mean_squared_error',
        "iteration_timeout_minutes": 30,
        "experiment_timeout_hours": 0.3,
        "featurization": featurization_config,
        "compute_target":cpu_cluster,
        "max_concurrent_iterations": 4,
        #"allowed_models":['Prophet'],
        "allowed_models":['Naive'],
        "blocked_models":['ExtremeRandomTrees', 'AutoArima', 'Prophet'],
        #"verbosity": logging.INFO,
        "training_data":ds,
        "label_column_name":label,
        "n_cross_validations": 3,
        "enable_voting_ensemble":True,
        "enable_early_stopping": False,
        "model_explainability":True,
        "enable_dnn":False,
        "forecasting_parameters": forecasting_parameters
            }

    automl_config = AutoMLConfig(**automl_settings)

    train_step = AutoMLStep(
            name='AutoML for time series forecast',
            automl_config=automl_config,    
            passthru_automl_config=False,    
            outputs=[metrics_data,model_data],    
            enable_default_model_output=True,
            enable_default_metrics_output=True,
            allow_reuse=True #if False, will trigger a new run, else re-use the existing output
        )

    # Register the model
    model_name = PipelineParameter("model_name", default_value="secondbestModel")
    register_model_step = PythonScriptStep(
            source_directory='.',
            script_name="./scripts/pipeline/register_model.py",
            name="Register the best model",
            arguments=[
                "--model_name", model_name,
                "--model_path", model_data
                ],
            inputs=[model_data],
            compute_target=cpu_cluster,
            runconfig=run_config,
            allow_reuse=False
            )

    experiment = Experiment(ws, name=experiment_name)
    pipeline = Pipeline(ws, [train_step, register_model_step])
    remote_run = experiment.submit(pipeline, show_output=True, wait_post_processing=True)
    remote_run.wait_for_completion()

# Setup experiment and trigger run
if __name__ == "__main__":
    main()
