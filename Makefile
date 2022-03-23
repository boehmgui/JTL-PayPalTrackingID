.PHONY: test
test:
	pytest -v --junitxml=pytest-results.xml tests/
