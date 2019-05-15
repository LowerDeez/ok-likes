coverage:
	coverage erase
	coverage run --rcfile=.coveragerc setup.py test
	coverage report
