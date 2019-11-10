all-tests:
	python3 run_all_tests.py

coverage:
	coverage run --source leaderboard,leaderboard_operation,exceptions,request_handler run_all_tests.py
	coverage html
	@echo "Coverage report done, please see htmlcov/index.html"
