import pytest
from pyspark.sql import SparkSession
from pyspark_data_processing.pipelines.data_processing.nodes import processar_info_corridas_do_dia
from tests.utils.moc_data import mock_df_para_processar_info_corridas_do_dia

# Setup SparkSession para testes
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("TestSession") \
        .master("local[2]") \
        .getOrCreate()


@pytest.mark.unit # Adicionado no pytest.ini para registro. Marca o teste como unitário, útil para categorizar testes.
def test_processar_info_corridas_do_dia(spark):

    input_df = mock_df_para_processar_info_corridas_do_dia(spark)

    expected_columns = {
        "DT_REFE",              # Data de referência.
        "QT_CORR",              # Quantidade de corridas.
        "QT_CORR_NEG",          # Quantidade de corridas com a categoria “Negócio”.
        "QT_CORR_PESS",         # Quantidade de corridas com a categoria “Pessoal”.
        "VL_MAX_DIST",          # Maior distância percorrida por uma corrida.
        "VL_MIN_DIST",          # Menor distância percorrida por uma corrida.
        "VL_AVG_DIST",          # Média das distâncias percorridas.
        "QT_CORR_REUNI",        # Quantidade de corridas com o propósito de "Reunião".
        "QT_CORR_NAO_REUNI"     # Quantidade de corridas com o propósito declarado e diferente de "Reunião".
    }

    result_df = processar_info_corridas_do_dia(input_df)

    # Extrai as colunas do dataframe de saída
    result_columns = set(result_df.columns)

    # Garante que o DataFrame de saída contenha exatamente as colunas esperadas
    assert result_columns == expected_columns
