install:
@pip install -r req.txt

run:
@alldata.append(zzone_type)

debug:
@python3 -d main.py

lint:
@flake8 .
@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
@