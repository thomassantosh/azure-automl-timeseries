"""Trigger the latest published pipeline"""
import sys
import os
import logging
from azureml.pipeline.core import PublishedPipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    """Get latest published pipeline, and submit pipeline"""
    # Get list of published pipelines, and select the first
    # Usually sorted in descending order
    try:
        published_pipelines = PublishedPipeline.list(workspace=ws)
        latest = published_pipelines[0]

        # Trigger/submit the published pipeline (without endpoint trigger)
        exp = latest.submit(workspace=ws, experiment_name='forecasting_for_energy_prices')
        logging.info(exp)
    except Exception as e:
        logging.warning(f'Error in submitting published pipeline. Message: {e}')

if __name__ == "__main__":
    main()
