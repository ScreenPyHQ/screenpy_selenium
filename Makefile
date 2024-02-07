# shortcuts
sync:
	poetry install --extras dev_all --sync

update_lock_only:
	poetry update --lock

update: update_lock_only
	poetry install --extras dev_all

check:
	poetry check

trunk_screenpy:
	poetry add screenpy git+ssh://git@github.com:ScreenPyHQ/screenpy.git#trunk

local_screenpy:
	pip uninstall screenpy
	pip install -e ~/projects/screenpy

.PHONY: sync update trunk_screenpy local_screenpy

black-check:
	black --check .

black:
	black .

isort-check:
	isort . --check

isort:
	isort .

ruff:
	ruff check .

ruff-fix:
	ruff check . --fix --show-fixes

mypy:
	mypy .

lint: isort-check ruff mypy

.PHONY: black-check black isort-check isort ruff ruff-fix mypy lint

pre-check-in: black-check lint

pre-check-in-fix: black isort ruff-fix mypy

.PHONY: pre-check-in pre-check-in-fix
