# kedro-pyspark-data-processing
# Pipeline de carregamento e processamento com PySpark e Kedro
## Strutura do Projeto

Projeto de pipeline de dados utilizando Kedro e PySpark para carregar, processar e gerar tabelas agregadas a partir de origens .csv, com foco em organização, modularidade, testes. O projeto foi feito utilizando o kedro 0.19.12 como framework base. 

```
kedro-pyspark-data-processing/
├── conf/
│   ├── README.md
│   ├── base/
│   │   ├── catalog.yml
│   │   ├── parameters.yml
│   │   └── spark.yml
│   └── local/
│       └── credentials.yml
├── data/
│   ├── processed/
│   │   └── .gitkeep
│   └── raw/
│       └── info_transportes.csv
├── src/
│   └── pyspark_data_processing/
│       ├── __init__.py
│       ├── __main__.py
│       ├── hooks.py
│       ├── pipeline_registry.py
│       ├── settings.py
│       └── pipelines/
│           ├── __init__.py
│           └── data_processing/
│               ├── nodes.py
│               └── pipeline.py
│       └── tests/
│           ├── common_tests/
│           │   ├── test_column_type_by_prefix.py
│           │   └── test_no_fully_null_columns.py
│           ├── test_nodes/
│           │   └── test_run.py
│           └── utils/
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
└── test_requirements.txt
```

---
## Gerando a imagem Docker

Na pasta onde encontra-se o DockerFile digitar o comando:
```powershell
docker build -t kedro-pyspark-data-processing .
```

## Execução com Docker
Necessário ter o docker instalado para build e run da imagem. No meu caso, instalei o docker desktop no windows, onde pode-se acompanhar containers e imagens.
Após instalação do docker, executa-se o seguinte comando, o comando deve ser executado na mesma pasta que está o DockerFile:

---
**PowerShell**:
```sh
docker run --rm -v ${PWD}/kedro-pyspark-data-processing/data:/app/kedro-pyspark-data-processing/data kedro-pyspark-data-processing
```
**Git Bash**:
```sh
docker run --rm -v "$(pwd)/kedro-pyspark-data-processing/data:/app/kedro-pyspark-data-processing/data" kedro-pyspark-data-processing
```
---

O projeto está salvando a tabela no caminho _kedro-pyspark-data-processing/data/processed_, que fica dentro do próprio projeto, o comando docker foi customizado para que o output fique persistido no próprio projeto.

Ao usar o parâmetro `-v` no `docker run`, mapeamos a pasta de dados do container para o projeto, garantindo que tudo que for salvo em processed dentro do container fica disponível no local indicado do projeto.

Ao executar o comando docker acima, ocorre o seguinte:
- O Kedro salva a tabela Delta em `/app/kedro-pyspark-data-processing/data/processed` (dentro do container).
- Com o volume, tudo que for salvo ali aparece em processed na sua máquina.
- Podemos abrir, ler, copiar ou versionar a tabela Delta normalmente após o pipeline rodar.

## Execução sem Docker - Configuração manual no Windows
Nesta sessão, será apresentado o passo a passo para rodar sem Docker, foi documentando os passos feitos para rodar manualmente no Windows. A imagem docker deste projeto foi construida com base na documentação feita abaixo, onde foi mapeando tudo que era necessário para rodar o spark, foi anotado todos os passos feitos para posteriormente construir a imagem docker da mesma maneira que foi configurado localmente.

### Pré-requisitos:
- [x] Download do Spark 3.4.4 com Scala 2.12: [Apache Spark Downloads](https://spark.apache.org/downloads.html)
- [x] Download do Python 3.11.9: [Python Downloads](https://www.python.org/downloads/windows/)
- [x] Download do Hadoop 3.3.5/bin (Windows): [WinUtils](https://github.com/cdarlint/winutils)
- [x] Download do Java JDK 17 (17.0.12): [Oracle JDK](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)

### Configuração das Variáveis de Ambiente

Os valores dependem do local de instalação. No meu caso:

| Variável        | Valor                              |
|-----------------|------------------------------------|
| `HADOOP_HOME`   | `C:\hadoop-3.3.5`                  |
| `JAVA_HOME`     | `C:\Program Files\Java\jdk-17`     |
| `PYSPARK_PYTHON`| `C:\Program Files\Python311\python.exe` |
| `PYTHON_HOME`   | `C:\Program Files\Python311`       |
| `SPARK_HOME`    | `C:\spark-3.4.4-bin-hadoop3`      |

### Configuração do PATH (adicionar):
```
C:\Program Files\Python311\Scripts\
C:\Program Files\Python311\
%JAVA_HOME%\bin
%HADOOP_HOME%\bin
%SPARK_HOME%\bin
%USERPROFILE%\AppData\Roaming\Python\Python311\Scripts
C:\Users\natan\AppData\Roaming\Python\Python311\Scripts
```

### Instalação dos Requirements

Navegue até a pasta contendo `requirements.txt` e execute:

```powershell
pip install -r requirements.txt
```

### Verificação da Instalação

Para confirmar que tudo está configurado corretamente:

```powershell
python -c "import pyspark; print(pyspark.__version__)"
```

### Rodar o projeto localmente
1. Rodar o comando abaixo:

   **Para Windows (PowerShell):**
   ```powershell
   $env:PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"
   ```

   **Para Bash (Linux/macOS):**
   ```bash
   export PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"
   ```

2. Rodar o comando abaixo (igual em todos os sistemas), o comando abaixo é executado na mesma pasta em que está o pyproject.toml:

   ```bash
   python -m kedro run
   ```

## Estratégia de testes
Neste projeto, adotamos o **pytest** como framework principal para testes em Python, complementado por plugins essenciais para garantia de qualidade.

Utilizamos os seguintes requirements para testes:

```python
pytest==7.4.4           # Framework base
pytest-cov==4.1.0       # Análise de cobertura
pytest-ordering==0.6    # Controle de ordem (não utilizado atualmente)
```

Onde:
- `pytest` - Roda os testes
- `pytest-cov` - Mede a cobertura de código
- `pytest-ordering` - Controla a ordem dos testes

### Ferramentas Utilizadas

#### **Pytest**
- Framework de testes para Python
- Permite escrever, organizar e rodar testes automatizados de forma simples e poderosa
- Comando principal:
  ```bash
  pytest
  ```

#### **pytest-cov**
- Plugin do pytest para medir a cobertura de código
- Mostra quais linhas do código foram executadas durante os testes
- Gera relatórios de cobertura no terminal ou em HTML
- Exemplo de uso:
  ```bash
  pytest --cov=src/
  ```

#### **pytest-ordering**
- Plugin para controlar a ordem de execução dos testes
- Permite definir ordem de execução com decorators
- Exemplo de uso:
  ```python
  @pytest.mark.run(order=1)
  def test_primeiro():
      ...
  ```

### Observação
No estado atual do projeto, não utilizamos o `pytest-ordering` pois não há necessidade de executar testes em sequência específica, mas mantemos nos requirements para completar o conjunto básico de ferramentas de teste, e para eventual necessidade futura.
Os nomes dos testes tem um prefixo padrão test_... indicando que é um teste.

## Executando o Pytest
Para rodar o pytest, pode-se seguir os seguintes passos:
Na pasta raíz do projeto, onde está src:

**PowerShell**
```powershell
$env:PYTHONPATH="src"; pytest -vv
```

**Git Bash**:
```bash
PYTHONPATH=src pytest -vv
```
No código acima, o parâmetro `-vv` (ou `--verbose --verbose`) após o comando `pytest` serve para deixar a saída **mais detalhada**.

- `pytest` mostra apenas o básico (pass/fail).
- `pytest -v` mostra o nome de cada teste.
- `pytest -vv` mostra ainda mais detalhes, como parâmetros de testes parametrizados, docstrings dos testes, e mensagens de assert.

Neste projeto, focamos sempre no usdo de pytest -vv para obter uma saída melhor detalhada dos testes.

## Cobertura de testes

```powershell
$env:PYTHONPATH="kedro-pyspark-data-processing/src"; coverage run -m pytest kedro-pyspark-data-processing/src/tests
```

```powershell
coverage report --show-missing
```

**Saída gerada do projeto:**
```
Name                                                                        Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------------------------
kedro-pyspark-data-processing\src\pyspark_data_processing\__init__.py                                 1      0   100%
kedro-pyspark-data-processing\src\pyspark_data_processing\pipelines\__init__.py                       0      0   100%
kedro-pyspark-data-processing\src\pyspark_data_processing\pipelines\data_processing\__init__.py       1      0   100%
kedro-pyspark-data-processing\src\pyspark_data_processing\pipelines\data_processing\nodes.py         19      8    58%   65-74
kedro-pyspark-data-processing\src\pyspark_data_processing\pipelines\data_processing\pipeline.py       4      1    75%   10
kedro-pyspark-data-processing\src\tests\common_tests\test_column_type_by_prefix.py           19      0   100%
kedro-pyspark-data-processing\src\tests\common_tests\test_no_fully_null_columns.py           14      0   100%
kedro-pyspark-data-processing\src\tests\test_nodes\test_run.py                               14      0   100%
kedro-pyspark-data-processing\src\tests\utils\moc_data.py                                     7      0   100%
---------------------------------------------------------------------------------------------------------
TOTAL                                                                          79      9    89%
```

## Encoding do CSV
Foi necessário realizar a verificação do encoding do .csv para correto carregamento no spark.
Ao utilizar um encoding diferente do correto, ocorre erros com caracteres estranhos, como: "ReuniÃ£o" em vez de "Reunião".

Código para checar o tipo de encoding:
```powershell
Get-Content -Path .\data\raw\info_transportes.csv -Encoding Byte -TotalCount 4 | Format-Hex
```
Resultado do comando: 00000000   EF BB BF 44   ï»¿D
significa que arquivo info_transportes.csv está codificado em UTF-8 com BOM (Byte Order Mark).

## SparkSession
Ao longo do desenvolvimento, foi feito múltiplas SparkSession em diferentes lugares, o que poderia causar inconsistências e desperdício de recursos, por isso, foi centralizado as configurações do spark no arquivo spark.yml, que usamos para criar a SparkSession apenas uma vez (no hook do Kedro ) e reutilizar essa sessão ao longo das execuções.
Assim, nos nodes acessamos a SparkSession já criada via context.spark (injeção de contexto)  e em em scripts externos, cria-se uma função utilitária para obter a SparkSession com as configurações corretas.
