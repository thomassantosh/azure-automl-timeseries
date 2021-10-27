# Publish the latest pipeline
from authentication import ws
from azureml.core.experiment import Experiment
from azureml.core import Run
from azureml.pipeline.core import PipelineRun
from azureml.train.automl.run import AutoMLRun
import pandas as pd
import logging, time
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Get pipeline runs from experiment
def experiment_details(sample_exp_name=None):
    collection_dict={}
    experiment_details = sample_exp_name.list(ws)
    for exp in experiment_details:
        get_run_details = exp.get_runs()
        for j,v in enumerate(get_run_details):
            parent_run_details = v.get_details()
            parent_run_status = parent_run_details['status']
            parent_runid = parent_run_details['runId']
            parent_end_time = parent_run_details['endTimeUtc']
            kv = str(exp) + '_' + str(v) + '_' + str(j)
            collection_dict[kv] = {
                    'experiment':str(exp), 
                    'parent_runId': parent_runid,
                    'parent_run_status':parent_run_status,
                    'parent_end_time':parent_end_time
                    }
    return pd.DataFrame(collection_dict)

def main():
    # Get latest completed pipeline run and the right run ID
    exp_name='forecasting_for_energy_prices'
    exp = Experiment(ws, name=exp_name)
    df = experiment_details(sample_exp_name=exp)
    df = df.T
    df = df[ df['parent_run_status'] == 'Completed'][:1].reset_index()
    run_id = df.at[0,'parent_runId']
    logging.info(f'PARENT RUN ID: {run_id}')

    # Get AutoMLStep Run ID
    pipeline_run = PipelineRun(experiment=exp, run_id = run_id)
    pipeline_steps = pipeline_run.get_steps()
    for l,x in enumerate(pipeline_steps):
        run_details = x.get_details()
        step_type = run_details['properties']['StepType']
        if step_type=="AutoMLStep":
            step_runid = run_details['runId']
            break
        else:
            step_runid = None
    logging.info(f'AutoMLStep run id: {step_runid}')

    # Get featurization summary details
    automl_run = AutoMLRun(experiment=exp, run_id=step_runid)
    best_run, fitted_model = automl_run.get_output()
    logging.info(f"Engg feature names:\n{fitted_model.named_steps['timeseriestransformer'].get_engineered_feature_names()}")
    logging.info(f"Featurization summary:\n{fitted_model.named_steps['timeseriestransformer'].get_featurization_summary()}")

if __name__ == "__main__":
    main()
