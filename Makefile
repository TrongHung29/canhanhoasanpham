.PHONY: all setup pipeline clean test setup-db download-data

all: pipeline

setup:
	pip install -r requirements.txt

setup-db:
	docker-compose up -d

pipeline:
	python -m backend.app.datagen
	python -m backend.app.quality
	python -m backend.app.train

test:
	pytest tests/

clean:
	rm -rf data/*
