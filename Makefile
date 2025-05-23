# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

pylint: venv
	# --disable=C0303,R0903,R0915,C0103,E1101,E0102,R0913,W0123,R0912,R0801 simulation map population
	./$(VENV)/bin/pylint smartanimations

create_scenes_app: venv
	./$(VENV)/bin/python3 manage.py startapp scenes

# tests: venv
#	./$(VENV)/bin/python3 -m unittest

tests: venv
	./$(VENV)/bin/pytest -q tests/tests.py tests/test_animation.py

run: venv
	./$(VENV)/bin/python3 manage.py runserver 8090

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

makemigrations: venv
	./$(VENV)/bin/python3 manage.py makemigrations
	./$(VENV)/bin/python3 manage.py sqlmigrate animations 0003  # change this
	./$(VENV)/bin/python3 manage.py sqlmigrate scenes 0001  # change this
	./$(VENV)/bin/python3 manage.py migrate

migrate: venv
	./$(VENV)/bin/python3 manage.py migrate

createsuperuser: venv
	./$(VENV)/bin/python3 manage.py createsuperuser

black-check:
	./$(VENV)/bin/python3 -m black --check setup scenes animations

black:
	./$(VENV)/bin/python3 -m black setup scenes animations


# make sure that all targets are used/evaluated even if a file with same name exists
.PHONY: all venv run clean tests black-check