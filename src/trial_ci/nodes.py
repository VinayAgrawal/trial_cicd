"""
This is a boilerplate pipeline
generated using Kedro 0.18.4
"""

import logging
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from pyspark.sql import DataFrame


def _species_count_validation(input_train_df: DataFrame):
    """Checks if data has more than 2 species in train data or not
    Args:
        input_train_df: input train data frame

    Returns:
        true if the count of species is greater than 2
    """
    species_count = input_train_df.select("species").distinct().count()

    if species_count > 2:
        return True


def split_data(data: DataFrame, parameters: Dict) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters.yml.
    Returns:
        Split data.
    """

    # Split to training and testing data
    data_train, data_test = data.randomSplit(
        weights=[parameters["train_fraction"], 1 - parameters["train_fraction"]]
    )

    if _species_count_validation(data_train):
        x_train = data_train.drop(parameters["target_column"])
        x_test = data_test.drop(parameters["target_column"])
        y_train = data_train.select(parameters["target_column"])
        y_test = data_test.select(parameters["target_column"])

        return x_train, x_test, y_train, y_test


def make_predictions(
    x_train: pd.DataFrame, x_test: pd.DataFrame, y_train: pd.DataFrame
) -> DataFrame:
    """Uses 1-nearest neighbour classifier to create predictions.

    Args:
        x_train: Training data of features.
        y_train: Training data for target.
        x_test: Test data for features.

    Returns:
        y_pred: Prediction of the target variable.
    """

    x_train_numpy = x_train.to_numpy()
    x_test_numpy = x_test.to_numpy()

    squared_distances = np.sum(
        (x_train_numpy[:, None, :] - x_test_numpy[None, :, :]) ** 2, axis=-1
    )
    nearest_neighbour = squared_distances.argmin(axis=0)
    y_pred = y_train.iloc[nearest_neighbour]
    y_pred.index = x_test.index

    return y_pred


def report_accuracy(y_pred: pd.Series, y_test: pd.Series):
    """Calculates and logs the accuracy.

    Args:
        y_pred: Predicted target.
        y_test: True target.
    """
    accuracy = (y_pred == y_test).sum() / len(y_test)
    logger = logging.getLogger(__name__)
    logger.info("Model has an accuracy of %.3f on test data.", accuracy)
