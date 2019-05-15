coverage:
	coverage erase
	coverage run --source='.' manage.py test likes
	coverage report
