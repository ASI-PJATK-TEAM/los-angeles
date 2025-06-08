"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from los_angeles.pipelines.data_processing import create_pipeline as data_processing_pipeline
from los_angeles.pipelines.data_science import create_pipeline as data_science_pipeline
from los_angeles.pipelines.reporting import create_pipeline as reporting_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": data_processing_pipeline() + data_science_pipeline() + reporting_pipeline(),
        "data_processing": data_processing_pipeline(),
        "data_science": data_science_pipeline(),
        "reporting": reporting_pipeline(),
    }
