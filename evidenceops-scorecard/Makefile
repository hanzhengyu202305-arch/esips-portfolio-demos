.PHONY: test report release-gate demo

test:
	python3 -m unittest discover -s tests -v

report:
	python3 -m evidenceops_scorecard.scorecard

release-gate:
	python3 -m evidenceops_scorecard.scorecard --release-gate

demo: report release-gate
