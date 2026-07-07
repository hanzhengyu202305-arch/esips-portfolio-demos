.PHONY: test demo report policy-pack

test:
	python3 -m unittest discover -s tests -v

demo:
	python3 -m kube_copilot.cli --out demo-output

report:
	python3 -m kube_copilot.risk_report

policy-pack:
	python3 -m kube_copilot.policy_pack
