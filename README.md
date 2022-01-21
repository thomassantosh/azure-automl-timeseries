# Intent
- Showcase Azure Machine Learning AutoML time series capabilities.
- Dataset is sourced from [here](http://mis.nyiso.com/public/P-58Blist.htm), and contains daily energy consumption
  data for 2020 across different East Coast counties and districts.
- These scripts do not extend into deploying the model through a web service or managed online endpoint. This
  is geared to understanding the workflows around training and prediction through the Python SDK.

# Notes
- Python version: `python=3.7`
- A pre-condition is to specify a `sub.env` file with `SUB=<your subscription id>` in the root of the folder.
- A Makefile shows the steps to create the infrastructure, run the pipeline and then use the best model to
  generate predictions.
- Though the `requirements.txt` exists to install all the needed libraries, the various stages of requiring
  various installs are shown below:
	- `pip install azureml-core` and `pip install python-dotenv` (before running `clusters.py`)
	- `pip install pandas` and `pip install azureml-dataset-runtime` (before running `datasets.py`)
	- `pip install azureml.train`, `pip install azureml.train.automl` and `pip install azureml.pipeline` (before running
	  `create_pipeline.py`)
	- `pip install matplotlib` (before running `metric_evaluation.py`)
  
## Final Prediction
![prediction](./model/final_result.png)
