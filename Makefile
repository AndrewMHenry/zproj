PYTHON = python3

.PHONY: clean clean-all install uninstall test

# recipe based on superuser "Delete matching files in all subdirectories"
# accepted answer
clean:
	find . -name \*~ -type f -delete
	find . -name \*.pyc -type f -delete

clean-all: clean
	rm -rf build
	rm -rf dist
	rm -rf zproj.egg-info
	rm -rf zproj/__pycache__
	rm -rf record.txt


install:
	$(PYTHON) setup.py install --record record.txt

# recipe from stackoverflow "python setup.py uninstall" accepted answer
uninstall: install
	cat record.txt | xargs rm -rf

test:
	$(PYTHON) -m unittest discover
