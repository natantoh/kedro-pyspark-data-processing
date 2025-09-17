from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, LongType

def processar_info_corridas_do_dia(df: DataFrame) -> DataFrame:

    """
    Recebe um dataframe, processa e salva uma tabela Delta agrupada por dia, a tabela final é particionada por DT_REFE.
    """
    
    # Extrai apenas o trecho da data com regex (seguro contra variações sutis)
    df = df.withColumn( 
        "DATA_SEM_HORA",
        f.regexp_extract("DATA_INICIO", r"(\d{1,2}-\d{1,2}-\d{4})", 1)
    )

    df = df.withColumn(
        "DT_REFE",
        f.to_date("DATA_SEM_HORA", "M-d-yyyy") # Aceita um ou dois dígitos para mês e dia
    )

    df = ( df
          .select(
            "DT_REFE",
            f.col("DISTANCIA").cast(DoubleType()).alias("DISTANCIA"),
            f.when(
                  f.trim(f.col("CATEGORIA")) == "Negocio", 1 
                  ).otherwise(0).alias("IN_NEGOCIO"),
            f.when(
                    f.trim(f.col("CATEGORIA")) == "Pessoal", 1
                    ).otherwise(0).alias("IN_PESSOAL"),
            f.when(
                    f.trim(f.col("PROPOSITO")) == "Reunião", 1
                    ).otherwise(0).alias("IN_REUNIAO"),
            f.when(
                    (f.col("PROPOSITO").isNotNull()) &
                    (f.trim(f.col("PROPOSITO")) != "") &
                    (f.trim(f.col("PROPOSITO")) != "Reunião"), 1
                    ).otherwise(0).alias("IN_NAO_REUNIAO")
                 )
            )

    result = (
        df.groupBy("DT_REFE")
        .agg(
            f.count("*").cast(LongType()).alias("QT_CORR"),
            f.sum("IN_NEGOCIO").cast(LongType()).alias("QT_CORR_NEG"),
            f.sum("IN_PESSOAL").cast(LongType()).alias("QT_CORR_PESS"),
            f.max("DISTANCIA").alias("VL_MAX_DIST"),
            f.min("DISTANCIA").alias("VL_MIN_DIST"),
            f.round( f.avg("DISTANCIA"), 2).alias("VL_AVG_DIST"),
            f.sum("IN_REUNIAO").cast(LongType()).alias("QT_CORR_REUNI"),
            f.sum("IN_NAO_REUNIAO").cast(LongType()).alias("QT_CORR_NAO_REUNI"),
        )
    )

    return result

def visualizar_info_corridas(delta_path: str) -> None:
    """
    Node de visualização que exibe o conteúdo da tabela Delta processada.
    Não retorna nada, apenas mostra os dados.
    """
    spark = SparkSession.getActiveSession()

    df = spark.read.format("delta").load(delta_path)

    print("="*80) # Imprime o caractere "=" 80 vezes
    print("Visualização da Tabela de Corridas Diárias")
    print("="*80)
    df.printSchema()
    df.show(truncate=False)
    print(f"\nTotal de dias registrados: {df.count()}")