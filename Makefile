.PHONY: up down sh run-etl logs restart

up:
	docker compose up --build -d

down:
	docker compose down

sh:
	docker exec -it test-data-engineering-loader-1 bash

run-etl:
	docker exec test-data-engineering-loader-1 python3 src/app/run_etl.py

logs:
	docker compose logs -f

restart:
	docker compose restart
