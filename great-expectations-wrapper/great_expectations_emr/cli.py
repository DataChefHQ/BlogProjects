import os
from collections import namedtuple
from datetime import datetime
from typing import List

from great_expectations import DataContext
from pyspark.sql import SparkSession

import typer
import yaml

from great_expectations_emr.helpers import get_relative_path
from great_expectations_emr.utils import update_ge_config

SuiteInfo = namedtuple(
    "SuiteInfo",
    ["suite_name", "database_name", "table_name"],
)


def get_suites(pipeline: str) -> List[SuiteInfo]:
    """Retrieve all the suites that are related to the provided pipeline

    :param pipeline: the pipeline to retrieve the suites for
    :return: A list of SuiteInfo tuples
    """
    suite_location = get_relative_path(f"suites/{pipeline}/{pipeline}_suites.yml")
    suites = load_suites_config(suite_location)
    return suites


def load_suites_config(suites_config_path: str) -> List[SuiteInfo]:
    """Read in the yaml suites an convert them to SuiteInfo tuples

    :param suites_config_path: the location of the suites
    :return: a list of SuitInfo tuples
    """
    with open(suites_config_path) as cp:
        suites = yaml.load(cp, Loader=yaml.FullLoader)

    suites = [SuiteInfo(**args) for args in suites]
    return suites


def get_run_id(suite: str, time_format: str = "%Y-%m-%d.%H:%M:%S") -> str:
    """Generate a run id based on the current suite and timestamp
    """
    timestamp = datetime.now().strftime(time_format)
    return f"{suite}.{timestamp}"


app = typer.Typer()
DEFAULT_SPARK_HOME = "/usr/lib/spark"
DEFAULT_CONTEXT_ROOT = get_relative_path("great_expectations")
APP_NAME = "great_expectations_wrapper"


@app.command(APP_NAME)
def run(
        pipeline: str = "",
        context_root_dir: str = DEFAULT_CONTEXT_ROOT,
        s3_bucket: str = None
):
    """Main function that holds the logic t

    :param pipeline: the pipeline for which to generate dashboards
    :param context_root_dir:
    :param s3_bucket:
    :return:
    """
    # Set the SPARK_HOME env var. This is necessary in EMR 6 since it's not already set
    current = os.environ.get("SPARK_HOME")
    if not current:
        os.environ["SPARK_HOME"] = DEFAULT_SPARK_HOME

    # You probably want to check if the pipeline is passed
    print(context_root_dir)
    suites = get_suites(pipeline)
    print("Suites have been loaded")

    keep_s3_history = False
    s3_prefix = "data_doc/"
    update_ge_config(context_root_dir, s3_bucket, keep_s3_history, s3_prefix)

    for suite in suites:
        print(f"Working on suite {suite}")
        result = generate_dashboard(
            suite.suite_name,
            suite.database_name,
            suite.table_name,
            app_name=APP_NAME,
            context_root_dir=context_root_dir
        )

        print("Success!") if result else print("Failed!")


def generate_dashboard(
        suite_name: str,
        database_name: str,
        table_name: str,
        app_name: str,
        spark_session: SparkSession = None,
        context_root_dir: str = "great_expectations"
) -> bool:
    if not spark_session:
        print("Creating spark session")
        spark_session = SparkSession.builder.appName(app_name) \
            .enableHiveSupport() \
            .getOrCreate()

    # Create a DataContext for the provided suite
    context = DataContext(context_root_dir)
    suite = context.get_expectation_suite(suite_name)
    df = spark_session.table(f"{database_name}.{table_name}")

    batch_kwargs = {"dataset": df, "datasource": "spark_datasource"}

    # Run the validation operator on the DataContext
    run_id = get_run_id(suite_name)
    batch = context.get_batch(batch_kwargs, suite)
    results = context.run_validation_operator(
        "action_list_operator", [batch], run_id=run_id
    )
    context.build_data_docs()

    print(results)

    if not results["success"]:
        print("No results")
        return False
    print("Data docs have been built")
    return True


def main():
    app()
