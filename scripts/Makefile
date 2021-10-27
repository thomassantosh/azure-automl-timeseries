install:
	#pip install --upgrade pip && pip install -r ./../requirements.txt
	./create-workspace-sprbac.sh

setup_run:
	python clusters.py
	python upload_data.py
	python datasets.py

create_pipeline:
	python create_pipeline.py

evaluation:
	python featurization.py
	python forecasting.py
	python metric_evaluation.py

publish_pipeline:
	python publish_pipeline.py

trigger_pipeline:
	python trigger_pipeline.py

all: install setup_run create_pipeline evaluation
run: create_pipeline evaluation
