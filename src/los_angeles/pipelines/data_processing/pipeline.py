from kedro.pipeline import Pipeline, node, pipeline

from .nodes import clean_crime_data, engineer_features, aggregate_crime

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
            ),
            node(
                func=aggregate_crime,
                inputs="crime_features",
                outputs="crime_aggregated",
                name="aggregated_crime_node"
            )
        ]
    )
