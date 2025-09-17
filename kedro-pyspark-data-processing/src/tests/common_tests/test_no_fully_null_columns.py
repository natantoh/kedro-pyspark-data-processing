import pytest
from pyspark.sql import SparkSession
from pyspark_data_processing.pipelines.data_processing.nodes import processar_info_corridas_do_dia
from tests.utils.moc_data import mock_df_para_processar_info_corridas_do_dia

# Setup SparkSession para todos os testes
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .appName("CommonValidationTests") \
        .master("local[2]") \
        .getOrCreate()


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
        # Adicione aqui outros casos:
        # pytest.param(mock_df_para_<outro>, processar_<outro>, "nome_identificador", id="nome_identificador")
    ]
)
def test_nenhuma_coluna_totalmente_nula(spark, dataframe_generator, transformer, label):
    """
    Teste genérico que garante que nenhuma coluna da saída está 100% nula.
    O label identifica qual conjunto de dados está sendo testado.
    """

    input_df = dataframe_generator(spark)

    # Executa a transformação
    result_df = transformer(input_df)

    # Verifica colunas totalmente nulas
    colunas_nulas = [
        col for col in result_df.columns
        if result_df.filter(f"{col} IS NOT NULL").count() == 0
    ]

    assert not colunas_nulas, (
        f"[{label}] Falha: as seguintes colunas estão totalmente nulas: {colunas_nulas}"
    )
