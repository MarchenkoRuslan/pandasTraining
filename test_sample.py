import pytest
import os
import main

files = main.files
pull = []

for file in os.listdir(files):
    if file.endswith(".csv"):
        pull += [file]


@pytest.mark.parametrize('dumple', pull)
def test_sample(dumple):
    path = files + file
    sheets = main.sheet_generator(path)
    main_sheet = main.sheets
    assert sheets == main_sheet
