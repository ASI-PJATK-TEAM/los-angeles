from kedro.pipeline import Pipeline, node, pipeline

from .nodes import prepare_model_input, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
            func=prepare_model_input,
            inputs="crime_features",
            outputs=["model_input_x", "model_input_y", "model_encoder"],
            name="prepare_model_input_node",
            ),
            node(
                func=train_model,
                inputs=["model_input_x", "model_input_y", "params:model_options"],
                outputs="crime_model",
                name="train_crime_model"
            )
        ]
    )
