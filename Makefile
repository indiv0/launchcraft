PC=python2.7

all: build

build: venv
	. venv/bin/activate; pyinstaller -F launchcraft.py

run: venv
	. venv/bin/activate; $(PC) launchcraft.py

venv: venv/bin/activate

venv/bin/activate:
	# Setup venv/ if it doesn't exist.
	test -d venv || virtualenv venv/ --python=$(PC)
	. venv/bin/activate; pip install -Ur requirements
	# Update file modification and access times.
	touch venv/bin/activate

clean:
	rm -rf venv/
	rm -rf logs/
	rm -rf build/
	rm -rf dist/
	rm -rf *.pyc
