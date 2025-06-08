"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.19.13
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa

from .nodes import generate_crime_score_distribution


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
                func=generate_crime_score_distribution,
                inputs="crime_model",
                outputs=None,
                name="generate_crime_score_distribution_node"
        )
    ])
