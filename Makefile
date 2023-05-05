MIN_PYTHON?=python3.8
TUTORIAL?=collapsable_tutorial
TUTORIAL_EXPANDING?=collapsable_expanding_tutorial
VENV?=venv

.PHONY: setup
setup: ## Install dependencies
	$(MIN_PYTHON) -m venv $(VENV)
	./$(VENV)/bin/python -m pip install -U pip
	./$(VENV)/bin/python -m pip install -r requirements.txt

.PHONY: setup-dev
setup-dev: ## Install dependencies
	$(MIN_PYTHON) -m venv $(VENV)
	./$(VENV)/bin/python -m pip install -U pip
	./$(VENV)/bin/python -m pip install -r requirements-dev.txt

.PHONY: run
run: ## Run the tutorial with --no-reload
	H2O_WAVE_NO_LOG=1 $(VENV)/bin/wave run --no-reload $(TUTORIAL)

.PHONY: run-expanding
run-expanding: ## Run the tutorial with --no-reload
	H2O_WAVE_NO_LOG=1 $(VENV)/bin/wave run --no-reload $(TUTORIAL_EXPANDING)

.PHONY: type-check
type-check: mypy ## Run static type check

.PHONY: mypy
mypy:
	@./$(VENV)/bin/mypy .

.PHONY: lint
lint: ## Run flake8
	@./$(VENV)/bin/mypy .  --exclude $(VENV)
	@./$(VENV)/bin/flake8 .  --exclude $(VENV)
	# @./$(VENV)/bin/black . --exclude $(VENV) --line-length 100 --check


.PHONY: format
format: ## Fix format of python files
	@./$(VENV)/bin/autoflake -i -r . --exclude $(VENV) --remove-all-unused-imports --verbose
	@./$(VENV)/bin/isort . --skip-glob $(VENV)
	@./$(VENV)/bin/black . --exclude $(VENV) --line-length 100

clean: ## Clean
	rm -rf $(VENV)
