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
    path = files + dumple
    sheets = main.sheet_generator(path)

    etalon_sheet = pd.read_excel('./etalon.xlsx', sheet_name=dumple)
    assert all(sheets[dumple] == etalon_sheet)

    etalon_sheet = pd.read_excel('./etalon.xlsx', sheet_name='Match ' + dumple)
    assert all(sheets['Match ' + dumple] == etalon_sheet)
