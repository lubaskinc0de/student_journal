all:
	pyinstaller student-journal.spec

test:
	pytest

lint:
	ruff format
	ruff check
	mypy
