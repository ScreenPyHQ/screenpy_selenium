# shortcuts to help manage flipping between branches with different dependencies
sync:
	poetry install --extras dev --sync

update_lock_only:
	poetry update --lock

update: update_lock_only
	poetry install --extras dev

check:
	poetry check

.PHONY: sync update_lock_only update check

black-check:
	black --check .

black-fix:
	black .

ruff-check:
	ruff check .

ruff-fix:
	ruff check . --fix --show-fixes

mypy:
	mypy .

.PHONY: black-check black-fix ruff-check ruff-fix mypy

pre-check-in: black-check ruff-check mypy

pre-check-in-fix: black-fix ruff-fix mypy

.PHONY: pre-check-in pre-check-in-fix

# requires poetry-plugin-export
requirements:
	poetry export --without-hashes --extras dev -f requirements.txt > requirements.txt

.PHONY: requirements

################################################################################
# sub-package specific

trunk_screenpy:
	poetry add screenpy git+ssh://git@github.com:ScreenPyHQ/screenpy.git#trunk

local_screenpy:
	pip uninstall screenpy
	pip install -e ~/projects/screenpy

.PHONY: trunk_screenpy local_screenpy
