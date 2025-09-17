from kedro.pipeline import Pipeline, node, pipeline  # Importa classes e funções para criar pipelines e nodes no Kedro

from .nodes import (
    processar_info_corridas_do_dia,                  # Importa a função processar_info_corridas_do_dia do módulo nodes
    visualizar_info_corridas,

)

def create_pipeline(**kwargs) -> Pipeline:           # Define uma função que cria e retorna um pipeline Kedro
    return pipeline(
        [
            node(
                func=processar_info_corridas_do_dia,         # Função que será executada neste node
                inputs="input_info_transportes",             # Nome do dataset de entrada (do Catalog)
                outputs="output_info_corridas_do_dia",       # Nome do dataset de saída (será salvo no Catalog)
                name="node_processar_info_corridas_do_dia",  # Nome identificador do node no pipeline
            ),
            node(
                func=visualizar_info_corridas,
                inputs=["params:delta_path"],
                outputs=None,
                name="node_visualizar_info_corridas",
            ),
        ]
    )
