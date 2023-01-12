"""
This module contains an example test.

Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.

To run the tests, run ``kedro test`` from the project root directory.
"""

from pathlib import Path

import pytest
from src.trial_ci.nodes import _species_count_validation
import pandas as pd
import pyspark
from pyspark.sql import SparkSession

@pytest.fixture()
def spark():
    """Spark Session"""
    return SparkSession.builder.config(
        "spark.sql.crossJoin.enabled", True
    ).getOrCreate()

@pytest.fixture()
def patient_data(spark: SparkSession) -> pyspark.sql.DataFrame:
    input_data = pd.DataFrame(
        {'sepal_length': [4.5, 3.5, 3.0, 2.9, 4.2],
         'sepal_width': [4.5, 3.5, 3.0, 2.9, 4.2],
         'petal_length': [4.5, 3.5, 3.0, 2.9, 4.2],
         'petal_width': [4.5, 3.5, 3.0, 2.9, 4.2],
         'species': ["spc1","spc2","spc3","spc2","spc3"],
         })

    input_data_spark = spark.createDataFrame(input_data)

    return input_data_spark

# The tests below are here for the demonstration purpose
# and should be replaced with the ones testing the project
# functionality

def test_species_count_validation(patient_data):
    # print("stupid life")
    # print(_species_count_validation(patient_data))
    assert _species_count_validation(patient_data)
