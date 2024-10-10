.PHONY: install start_localstack tf_apply lint type_check test all_checks
TERRAFORM_DIR = terraform/

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt || true
	.venv/bin/pip install -r requirements-dev.txt || true
	start_localstack
	mkdir -p $(TERRAFORM_DIR)zipped_lambda_code/sqs_to_dynamodb/
	zip_lambdas
	tflocal -chdir=$(TERRAFORM_DIR) init
	tflocal -chdir=$(TERRAFORM_DIR) apply

start_localstack:
	#docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
	docker compose up

zip_lambdas:
	zip -j -q -r $(TERRAFORM_DIR)zipped_lambda_code/sqs_to_dynamodb/lambda.zip lambdas/sqs_to_dynamodb/lambda_function.py

tf_apply:
	tflocal -chdir=$(TERRAFORM_DIR) apply	

lint:
	pylint . || true
	flake8 || true

check_types:
	mypy . || true

test:
	PYTHONPATH=$(shell pwd)/vehicles_simulator:$(shell pwd) pytest vehicles_simulator/tests/ || true

check_all: test check_types lint
