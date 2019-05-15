coverage:
	coverage erase
	coverage run -m django test --settings=likes.tests.settings
	coverage report
