install:
	@pip install -r req.txt

run:
	@python3 src/main.py

debug:
	@python3 -d src/main.py

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@rm -rf */__pycache__