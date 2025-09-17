# Makefile para automação de comandos do projeto kedro-pyspark-data-processing
# Utilize 'make <alvo>' no terminal (Git Bash, WSL ou Linux/Mac)
# Cada comando está comentado para facilitar o entendimento.

# Instala os requirements
install:
	pip install -r kedro-pyspark-data-processing/requirements.txt

# Executar fora do docker
run:
	cd kedro-pyspark-data-processing; python -m kedro run

# Gera a imagem Docker
docker-build:
	docker build -t kedro-pyspark-data-processing .

# Roda via docker ( No Maker não interpreta o PWD, por isso precisa copiar e colar no terminal)
docker-run:
	docker run --rm -v ${PWD}/kedro-pyspark-data-processing/data:/app/kedro-pyspark-data-processing/data kedro-pyspark-data-processing

# Instala os requirements
install-test:
	pip install -r kedro-pyspark-data-processing/test_requirements.txt

# Executa todos os testes
test-full:
	$env:PYTHONPATH="src"; pytest -vv

# Executa o teste test_column_type_by_prefix
test-prefix:
	$env:PYTHONPATH="src"; pytest -vv src/tests/common_tests/test_column_type_by_prefix.py

# Executa o teste test_no_fully_null_columns
test-null:
	$env:PYTHONPATH="src"; pytest -vv src/tests/common_tests/test_no_fully_null_columns.py

# Executa o test_run
test-node-run:
	$env:PYTHONPATH="src"; pytest -vv src/tests/test_nodes/test_run.py

.PHONY: install run docker-build docker-run install-test test-full test-prefix test-null test-node-run