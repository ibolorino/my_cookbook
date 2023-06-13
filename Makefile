clean:
	@echo "Execute cleaning ..."
	rm -f *.pyc
	rm -f .coverage
	rm -f coverage.xml

lint:
	flake8 --config setup.cfg .
	isort . --check

test: clean
	pytest --cov-config=setup.cfg --cov=my_cookbook tests/

coverage: clean lint
	pytest --cov-config=setup.cfg --cov=my_cookbook tests/ --cov-report=html --cov-report=xml

dependencies:
	docker-compose up -d

format: clean
	isort .

runserver:
	uvicorn wsgi:application --reload

down:
	docker-compose down
