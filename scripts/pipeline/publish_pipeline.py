# Publish the latest pipeline
import sys
import os
import logging, time
from azureml.core.experiment import Experiment
from azureml.pipeline.core import PipelineRun
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Get pipeline runs from experiment
def experiment_details(sample_exp_name=None):
    collection_dict={}
    exp_details = sample_exp_name.list(ws)
    for exp in exp_details:
        get_run_details = exp.get_runs()
        for j,v in enumerate(get_run_details):
            parent_run_details = v.get_details()
            parent_run_status = parent_run_details['status']
            parent_runid = parent_run_details['runId']
            parent_end_time = parent_run_details['endTimeUtc']
            keyvalue = str(exp) + '_' + str(v) + '_' + str(j)
            collection_dict[keyvalue] = {
                    'experiment':str(exp),
                    'parent_runId': parent_runid,
                    'parent_run_status':parent_run_status,
                    'parent_end_time':parent_end_time
                    }
    return pd.DataFrame(collection_dict)

def main():
    exp_name='forecasting_for_energy_prices'
    exp = Experiment(ws, name=exp_name)
    data_frame = experiment_details(sample_exp_name=exp)
    data_frame = data_frame.T

    # Get latest completed pipeline run and the right run ID
    data_frame = data_frame[ data_frame['parent_run_status'] == 'Completed'][:1].reset_index()
    run_id = data_frame.at[0,'parent_runId']
    logging.info(f'Run ID is: {run_id}')

    pipeline_run = PipelineRun(experiment=exp, run_id = run_id)

    #Publish the latest completed pipeline
    try:
        pipeline_run.publish_pipeline(
                name='forecasting_energy_' + str(int(time.time())),
                description="Pipeline for forecasting energy prices",
                version="latest")
    except Exception as e:
        logging.warning(e)

if __name__ == "__main__":
    main()
