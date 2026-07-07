PYTHON ?= python3
SCENARIO ?= S1
MODE ?= multi
QUERY ?= CrashLoopBackOff invalid environment variable
RUNS ?= 3

.PHONY: help setup quickstart acceptance test test-app lint build-index retrieve scenario collect-evidence demo validate eval-mock matrix doctor triage scorecard poc-repro poc docker-build kind-setup report issue-to-pr-report serve-app

help:
	@$(PYTHON) -m agent.main help

setup:
	$(PYTHON) -m pip install -e .

quickstart: doctor test build-index matrix
	$(PYTHON) -m agent.main demo --scenario S4 --mode multi
	$(PYTHON) -m agent.main eval-mock
	$(PYTHON) -m agent.main report
	@echo "Quickstart complete. Read docs/NEWCOMER_GUIDE.zh-CN.md and reports/final-portfolio-report.md"

acceptance:
	$(PYTHON) -m agent.main acceptance

test:
	$(PYTHON) -m pytest tests apps/demo-api/tests -q

test-app:
	$(PYTHON) -m pytest apps/demo-api/tests -q

lint:
	$(PYTHON) scripts/lint.py

build-index:
	$(PYTHON) -m agent.main build-index

retrieve:
	$(PYTHON) -m agent.main retrieve --query "$(QUERY)"

scenario:
	$(PYTHON) -m agent.main scenario --scenario $(SCENARIO)

collect-evidence:
	$(PYTHON) -m agent.main collect-evidence --scenario $(SCENARIO)

demo:
	$(PYTHON) -m agent.main demo --scenario $(SCENARIO) --mode $(MODE)

validate:
	$(PYTHON) -m agent.main validate --scenario $(SCENARIO) --mode $(MODE)

eval-mock:
	$(PYTHON) -m agent.main eval-mock

scorecard:
	$(PYTHON) -m agent.main scorecard

poc-repro:
	$(PYTHON) -m agent.main poc-repro --runs $(RUNS)

poc: poc-repro

matrix:
	$(PYTHON) -m agent.main matrix

doctor:
	$(PYTHON) -m agent.main doctor

triage:
	$(PYTHON) -m agent.main triage

docker-build:
	$(PYTHON) scripts/docker_build_or_dry_run.py

kind-setup:
	$(PYTHON) scripts/setup_kind.py

report:
	$(PYTHON) -m agent.main report

issue-to-pr-report:
	$(PYTHON) -m agent.main demo --scenario S4 --mode multi
	$(PYTHON) -m agent.main report

serve-app:
	PYTHONPATH=apps/demo-api APP_MODE=demo $(PYTHON) -m uvicorn app.main:app --reload --port 8000
