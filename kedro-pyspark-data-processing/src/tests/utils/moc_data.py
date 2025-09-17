from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Cria uma sessão Spark local para teste
spark = SparkSession.builder \
    .appName("MockTest") \
    .master("local[*]") \
    .getOrCreate()

def mock_df_para_processar_info_corridas_do_dia(spark: SparkSession):
    """Cria e retorna um DataFrame simulado com 10 linhas variadas"""

    schema = StructType([
        StructField("DATA_INICIO", StringType(), True),
        StructField("DATA_FIM", StringType(), True),
        StructField("CATEGORIA", StringType(), True),
        StructField("LOCAL_INICIO", StringType(), True),
        StructField("LOCAL_FIM", StringType(), True),
        StructField("DISTANCIA", DoubleType(), True),
        StructField("PROPOSITO", StringType(), True)
    ])

    data = [
        {"DATA_INICIO": "01-05-2016 08:00", "DATA_FIM": "01-05-2016 08:30", "CATEGORIA": "Negocio", "LOCAL_INICIO": "Fort Pierce", "LOCAL_FIM": "Raleigh", "DISTANCIA": 12.5, "PROPOSITO": "Alimentação"},
        {"DATA_INICIO": "01-05-2016 09:00", "DATA_FIM": "01-05-2016 09:20", "CATEGORIA": "Pessoal", "LOCAL_INICIO": "Cary", "LOCAL_FIM": "Raleigh", "DISTANCIA": 8.0, "PROPOSITO": ""},
        {"DATA_INICIO": "01-05-2016 10:00", "DATA_FIM": "01-05-2016 10:25", "CATEGORIA": "Negocio", "LOCAL_INICIO": "New York", "LOCAL_FIM": "West Palm Beach", "DISTANCIA": 15.0, "PROPOSITO": None},
        {"DATA_INICIO": "02-05-2016 11:00", "DATA_FIM": "02-05-2016 11:45", "CATEGORIA": "Pessoal", "LOCAL_INICIO": "Flatiron District", "LOCAL_FIM": "Hell's Kitchen", "DISTANCIA": 20.0, "PROPOSITO": "Reunião"},
        {"DATA_INICIO": "02-05-2016 12:00", "DATA_FIM": "02-05-2016 12:35", "CATEGORIA": "Negocio", "LOCAL_INICIO": "Downtown", "LOCAL_FIM": "Midtown", "DISTANCIA": 25.0, "PROPOSITO": "Visita ao cliente"},
        {"DATA_INICIO": "02-05-2016 13:00", "DATA_FIM": "02-05-2016 13:15", "CATEGORIA": "Negocio", "LOCAL_INICIO": "Houston", "LOCAL_FIM": "Raleigh", "DISTANCIA": 5.0, "PROPOSITO": "Parada temporária"},
        {"DATA_INICIO": "03-05-2016 14:00", "DATA_FIM": "03-05-2016 14:40", "CATEGORIA": "Pessoal", "LOCAL_INICIO": "Eagan Park", "LOCAL_FIM": "Hudson Square", "DISTANCIA": 10.0, "PROPOSITO": "Entre escritórios"},
        {"DATA_INICIO": "03-05-2016 15:00", "DATA_FIM": "03-05-2016 15:30", "CATEGORIA": "Negocio", "LOCAL_INICIO": "Gulfton", "LOCAL_FIM": "Lower Manhattan", "DISTANCIA": 18.0, "PROPOSITO": "Caridade"},
        {"DATA_INICIO": "04-05-2016 16:00", "DATA_FIM": "04-05-2016 16:30", "CATEGORIA": "Pessoal", "LOCAL_INICIO": "Jamaica", "LOCAL_FIM": "Lower Manhattan", "DISTANCIA": 22.0, "PROPOSITO": "Deslocamento"},
        {"DATA_INICIO": "04-05-2016 17:00", "DATA_FIM": "04-05-2016 17:50", "CATEGORIA": "Negocio", "LOCAL_INICIO": "Jamaica", "LOCAL_FIM": "Midtown East", "DISTANCIA": 30.0, "PROPOSITO": "Aeroporto/Viagem"},
    ]

    return spark.createDataFrame(data, schema=schema)