# -----------------------------------------------------------------------------
#                                   CHECKS
# -----------------------------------------------------------------------------
.PHONY: lint
lint:
	ruff check dashboard_service tests

.PHONY: type
type:
	mypy dashboard_service

.PHONY: test
test:
	python -mpytest tests

.PHONY: check
check: test lint type

# -----------------------------------------------------------------------------
#                                  UTILS
# -----------------------------------------------------------------------------
.PHONY: dump_config
dump_config:
	@python -m dashboard_service.cli --dump-default-config

.PHONY: format
format: ## Fix code style violations with ruff and black
	ruff check --select I --fix dashboard_service tests
	black dashboard_service tests

.PHONY: run
run:
	@DASHBOARD_SERVICE_CONFIG=examples/dashboard_service.yaml uvicorn --reload --port 6384 dashboard_service.main:app

.PHONY: image
image:
	@docker build --secret id=PIP_INDEX_URL -t dashboard_service:dev .

