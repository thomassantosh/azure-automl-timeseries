install:
	pip install --upgrade pip && pip install -r requirements.txt

setup_infra:
	./scripts/setup/create-workspace-sprbac.sh

lint:
	pylint --disable=R,C,W1203,W0702 upload_data.py
	pylint --disable=R,C,W1203,W0702 datasets.py
	pylint --disable=R,C,W1203,W0702 clusters.py

setup_run:
	python ./scripts/setup/clusters.py
	python ./scripts/setup/upload_data.py
	python ./scripts/setup/datasets.py

create_pipeline:
	python ./scripts/pipeline/create_pipeline.py

evaluation:
	python featurization.py
	python forecasting.py
	python metric_evaluation.py

publish_pipeline:
	python publish_pipeline.py

trigger_pipeline:
	python trigger_pipeline.py

all: install setup_infra setup_run create_pipeline evaluation
run: create_pipeline evaluation
