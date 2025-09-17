import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, LongType, FloatType, DoubleType, DecimalType, StringType, DateType
from pyspark_data_processing.pipelines.data_processing.nodes import processar_info_corridas_do_dia
from tests.utils.moc_data import mock_df_para_processar_info_corridas_do_dia

# Setup SparkSession para todos os testes
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("CommonValidationTests") \
        .master("local[2]") \
        .getOrCreate()

# Define os tipos esperados para cada prefixo
TYPE_RULES = {
    "QT": (IntegerType, LongType),
    "VL": (FloatType, DoubleType, DecimalType),
    "DT": (StringType, DateType),
}

@pytest.mark.unit
@pytest.mark.parametrize(
    "dataframe_generator, transformer, label",
    [
        pytest.param(
            mock_df_para_processar_info_corridas_do_dia,
            processar_info_corridas_do_dia,
            "info_corridas_do_dia",
            id="info_corridas_do_dia"
        ),
        # Adicione outros testes aqui
    ]
)
def test_prefix_type_rules(spark, dataframe_generator, transformer, label):
    """
    Valida se colunas com prefixo QT, VL e DT têm os tipos esperados.
    """

    input_df = dataframe_generator(spark)
    result_df = transformer(input_df)

    for field in result_df.schema.fields:
        prefix = field.name[:2]
        expected_types = TYPE_RULES.get(prefix)

        if expected_types:
            assert isinstance(field.dataType, expected_types), (
                f"[{label}] Coluna '{field.name}' deveria ser do tipo {expected_types}, "
                f"mas é {type(field.dataType)}"
            )
