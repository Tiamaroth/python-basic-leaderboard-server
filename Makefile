all-tests:
	python3 run_all_tests.py

coverage:
	coverage run --source leaderboard,server run_all_tests.py
	coverage html
	@echo "Coverage report done, please see htmlcov/index.html"
