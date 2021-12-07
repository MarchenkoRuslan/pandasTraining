import pytest
import pandas as pd
import os
import main
from pandas.testing import assert_frame_equal
from pandas.api.types import CategoricalDtype

files = main.files
pull = []
data_types = {'AccountNumber': 'object',
              'SecurityCode': CategoricalDtype(categories=['EF', 'MF', 'OT'], ordered=False),
              'Price': 'float64',
              'TransactionDate': 'object',
              '_merge': CategoricalDtype(categories=['left_only', 'right_only', 'both'], ordered=False)}

for file in os.listdir(files):
    if file.endswith(".csv"):
        pull += [file]


@pytest.mark.parametrize('dumple', pull)
def test_sample(dumple):
    path = files + dumple
    sheets = main.sheet_generator(path)
    etalon_sheet = pd.read_excel('./etalon.xlsx', sheet_name=dumple)
    assert_frame_equal(sheets[dumple], etalon_sheet)

    etalon_sheet = pd.read_excel('./etalon.xlsx', sheet_name='Match ' + dumple, converters={'AccountNumber': str})
    sheets['Match ' + dumple] = sheets['Match ' + dumple].astype(data_types)
    etalon_sheet = etalon_sheet.astype(data_types)
    assert_frame_equal(sheets['Match ' + dumple], etalon_sheet)
