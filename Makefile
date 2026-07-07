AEGISOPS_PY ?= /opt/anaconda3/bin/python3.13

.PHONY: test root-test reports demo-all public-boundary-check portfolio-check aegisops-test kube-test haul-test evidenceops-test

test: root-test aegisops-test kube-test haul-test evidenceops-test

root-test:
	python3 -m unittest discover -s tests -v

aegisops-test:
	$(MAKE) -C aegisops-agent test PYTHON=$(AEGISOPS_PY)

kube-test:
	$(MAKE) -C kube-copilot test

haul-test:
	$(MAKE) -C haul-truck-planner test

evidenceops-test:
	$(MAKE) -C evidenceops-scorecard test

reports:
	$(MAKE) -C aegisops-agent report PYTHON=$(AEGISOPS_PY)
	$(MAKE) -C kube-copilot report
	$(MAKE) -C kube-copilot policy-pack
	$(MAKE) -C haul-truck-planner report
	$(MAKE) -C evidenceops-scorecard report

demo-all:
	python3 scripts/demo_all.py --aegisops-python "$(AEGISOPS_PY)"

public-boundary-check:
	python3 scripts/public_boundary_check.py

portfolio-check:
	AEGISOPS_STABLE_REPORTS=1 python3 scripts/portfolio_check.py --aegisops-python "$(AEGISOPS_PY)"
