install:
	pip install --upgrade pip && pip install -r requirements.txt

setup_infra:
	./scripts/setup/create-workspace-sprbac.sh

lint:
	pylint --disable=R,C,W1203,W0702,W0703 ./scripts/setup/upload_data.py
	pylint --disable=R,C,W1203,W0702,W0703 ./scripts/setup/datasets.py
	pylint --disable=R,C,W1203,W0702,W0703,E0110 ./scripts/setup/clusters.py

setup_run:
	python ./scripts/setup/clusters.py
	python ./scripts/setup/upload_data.py
	python ./scripts/setup/datasets.py

create_pipeline:
	python ./scripts/pipeline/create_pipeline.py

publish_pipeline:
	python ./scripts/pipeline/publish_pipeline.py

trigger_pipeline:
	python ./scripts/pipeline/trigger_pipeline.py

evaluation:
	python ./scripts/prediction/featurization.py
	python ./scripts/prediction/forecasting.py
	python ./scripts/prediction/metric_evaluation.py

all: install setup_infra setup_run create_pipeline evaluation
run: create_pipeline evaluation
