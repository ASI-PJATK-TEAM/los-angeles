from kedro.pipeline import Pipeline, node, pipeline

from .nodes import clean_crime_data, engineer_features


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_crime_data,
                inputs="crime_raw",
                outputs="crime_clean",
                name="clean_crime_data_node",
            ),
            node(
                func=engineer_features,
                inputs="crime_clean",
                outputs="crime_features",
                name="engineer_features_node"
            )
        ]
    )
