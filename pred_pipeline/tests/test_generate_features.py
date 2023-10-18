import pandas as pd
import numpy as np
import pytest
from src.generate_features import generate_features


# Happy
def test_basic_operation():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}).astype(float)

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {"operation": "multiply", "source1": "A", "source2": "B", "target": "D"}
        ],
    }

    result = generate_features(data, config)
    expected_result = pd.DataFrame(
        {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9], "D": [4, 10, 18]}
    ).astype(float)

    assert result.equals(expected_result)


def test_nested_operation():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}).astype(float)

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {
                "operation": "multiply",
                "source1": {"operation": "subtract", "source1": "A", "source2": "B"},
                "source2": "B",
                "target": "D",
            }
        ],
    }

    result = generate_features(data, config)
    expected_result = pd.DataFrame(
        {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9], "D": [-12, -15, -18]}
    ).astype(float)

    assert result.equals(expected_result)


def test_apply_operation():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}).astype(float)

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {"target": "D", "operation": "apply", "source1": "A", "function": "square"}
        ],
    }

    result = generate_features(data, config)
    expected_result = pd.DataFrame(
        {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9], "D": [1, 4, 9]}
    ).astype(float)

    assert result.equals(expected_result)


def test_multiple_operations():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}).astype(float)

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {
                "operation": "multiply",
                "source1": "A",
                "source2": "B",
                "target": "D",
            },
            {
                "operation": "subtract",
                "source1": "A",
                "source2": "B",
                "target": "E",
            },
        ],
    }

    result = generate_features(data, config)
    expected_result = pd.DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8, 9],
            "D": [4, 10, 18],
            "E": [-3, -3, -3],
        }
    ).astype(float)

    pd.testing.assert_frame_equal(result, expected_result)


def test_divide_operation():
    data = pd.DataFrame({"A": [2, 4, 6], "B": [4, 8, 12], "C": [1, 2, 3]}).astype(float)

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {"target": "D", "operation": "divide", "source1": "B", "source2": "A"}
        ],
    }

    result = generate_features(data, config)
    expected_result = pd.DataFrame(
        {"A": [2, 4, 6], "B": [4, 8, 12], "C": [1, 2, 3], "D": [2, 2, 2]}
    ).astype(float)

    pd.testing.assert_frame_equal(result, expected_result)


# Unhappy
def test_missing_feature_col():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    config = {
        "feature_col": "A",
        "target_col": "C",
        "feature_eng": [
            {"target": "D", "operation": "multiply", "source1": "A", "source2": "B"}
        ],
    }

    with pytest.raises(KeyError):
        result = generate_features(data, config)


def test_invalid_operation():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {
                "target": "D",
                "operation": "invalid_operation",
                "source1": "A",
                "source2": "B",
            }
        ],
    }

    with pytest.raises(NotImplementedError):
        result = generate_features(data, config)


def test_invalid_function():
    data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    config = {
        "feature_col": ["A", "B"],
        "target_col": "C",
        "feature_eng": [
            {
                "target": "D",
                "operation": "apply",
                "source1": "A",
                "function": "invalid_function",
            }
        ],
    }

    with pytest.raises(AttributeError):
        result = generate_features(data, config)
