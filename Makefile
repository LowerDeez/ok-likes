coverage:
	coverage erase
	coverage run --rcfile=.coveragerc --append runtests.py
	coverage report
