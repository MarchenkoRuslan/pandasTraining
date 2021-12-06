import pytest
import pandas as pd
import os
import main

files = main.files
pull = []

for file in os.listdir(files):
    if file.endswith(".csv"):
        pull += [file]


@pytest.mark.parametrize('dumple', pull)
def test_sample(dumple):
    sample = main.sample
    path = files + file

    dumple = pd.read_csv(path)
    dumple = main.fix(sample, dumple)

    assert all(dumple.dtypes == sample.dtypes)
