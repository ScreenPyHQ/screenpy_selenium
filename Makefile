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