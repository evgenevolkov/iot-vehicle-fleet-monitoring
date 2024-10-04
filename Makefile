.PHONY: install lint type_check test all_checks

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt || true
	.venv/bin/pip install -r requirements-dev.txt || true

lint:
	pylint . || true
	flake8 || true

check_types:
	mypy . || true

test:
	PYTHONPATH=$(shell pwd)/vehicles_simulator pytest vehicles_simulator/tests/functional/ || true

check_all: test check_types lint
