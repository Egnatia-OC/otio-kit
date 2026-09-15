.PHONY: lint test build compile-golden clean

lint:
	ruff check core tests

test:
	pytest tests/ -q

build:
	python -m build

# regenerate the committed golden file after an INTENTIONAL emitter change
compile-golden:
	PYTHONPATH=core python -m otio_kit.cli compile tests/golden/specimen60.yaml \
		-o tests/golden/specimen60.golden.otio

clean:
	rm -rf build dist *.egg-info core/*.egg-info .pytest_cache
	find . -name __pycache__ -type d -exec rm -rf {} +
