import pytest
import pandas as pd
import os
import main


# @pytest.fixture(scope="module")
# def fixture():
#
#     return [sample, files, col_order, data_types, dumple]


def test_sample():
    sample = main.sample
    files = main.files

    for file in os.listdir(files):
        if file.endswith(".csv"):
            path = files + file
            dumple = pd.read_csv(path)
            dumple = main.fix(sample, dumple)

            for col in dumple:
                assert dumple[col].dtype == sample[col].dtype
