.PHONY: install dev test lint

install:
	pip install -r requirements.txt

dev:
	uvicorn api.main:app --reload --port 8002

test:
	pytest tests/ -v

lint:
	ruff check .
