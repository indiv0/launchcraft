PC=python2.7

all: build

build: venv
	. venv/bin/activate; pyinstaller launchcraft.spec

run: venv
	. venv/bin/activate; $(PC) launchcraft.py

venv: venv/bin/activate

venv/bin/activate:
	# Setup venv/ if it doesn't exist.
	test -d venv || virtualenv2 venv/ --python=$(PC)
	. venv/bin/activate; pip install -Ur requirements
	# Update file modification and access times.
	touch venv/bin/activate
	cp venv/lib/python2.7/site-packages/certifi/cacert.pem cacert.pem

fullclean: clean
	rm -rf venv/
	rm -rf cacert.pem

clean:
	rm -rf logs/
	rm -rf build/
	rm -rf dist/
	rm -rf *.pyc
	rm -rf *.zip
