install:
	@python3 -m pip install pydantic flake8 mypy

run:
	@python3 src/main.py

debug:
	@python3 -m pdb src/main.py

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@rm -rf */__pycache__ __pycache__ 
	@rm -rf */.mypy_cache .mypy_cache