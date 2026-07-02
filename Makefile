AEGISOPS_PY ?= /opt/anaconda3/bin/python3.13

.PHONY: test reports aegisops-test kube-test haul-test

test: aegisops-test kube-test haul-test

aegisops-test:
	$(MAKE) -C aegisops-agent test PYTHON=$(AEGISOPS_PY)

kube-test:
	$(MAKE) -C kube-copilot test

haul-test:
	$(MAKE) -C haul-truck-planner test

reports:
	$(MAKE) -C aegisops-agent report PYTHON=$(AEGISOPS_PY)
	$(MAKE) -C kube-copilot report
	$(MAKE) -C haul-truck-planner report
