import pandas as pd
import os
from pandas.api.types import CategoricalDtype

files = 'files/'
match = pd.DataFrame()

sample = pd.read_csv('sample_file.csv')
report = pd.DataFrame([['sample_file.csv', len(sample.index),
                        sample['AccountNumber'].dtype, sample['SecurityCode'].dtype,
                        sample['Price'].dtype, sample['TransactionDate'].dtype]],
                      columns=['File name', 'Row count', 'AccountNumber', 'SecurityCode', 'Price', 'TransactionDate'])

sheets = {'sample_file.csv': report}

status_type = CategoricalDtype(categories=['EF', 'MF', 'OT'], ordered=False)
col_order = ['AccountNumber', 'SecurityCode', 'Price', 'TransactionDate']
data_types = {'AccountNumber': 'object',
              'SecurityCode': status_type,
              'Price': 'float64',
              'TransactionDate': 'datetime64'}


def fix(sample, dumple):
    if len(sample.columns) < len(dumple.columns):
        for col in dumple:
            if col not in col_order:
                del dumple[col]
    elif len(sample.columns) > len(dumple.columns):
        find = set(sample.columns) - set(dumple.columns)
        dumple[list(find)] = None
        dumple = dumple[col_order]
    else:
        if tuple(dumple.columns) != tuple(col_order) and dumple.columns.all() in col_order:
            dumple = dumple[col_order]
        else:
            dumple = pd.read_csv(path, names=col_order, header=0)

    dumple = dumple.loc[dumple['AccountNumber'] != "AccountNumber"]
    dumple = dumple.astype(data_types)
    return dumple


sample = sample.astype(data_types)

for file in os.listdir(files):
    if file.endswith(".csv"):
        path = files + file
        dumple = pd.read_csv(path)
        sheets[file] = pd.DataFrame([file, len(dumple.index), [dumple[col].dtype for col in list(dumple)]],
                                    columns=['File name', 'Row count', [col for col in list(dumple)]])

        print(file)
        dumple = fix(sample, dumple)

        # addon = pd.DataFrame([[file, len(dumple.index),
        #                        dumple['AccountNumber'].dtype, dumple['SecurityCode'].dtype,
        #                        dumple['Price'].dtype, dumple['TransactionDate'].dtype]],
        #                      columns=['File name', 'Row count', 'AccountNumber', 'SecurityCode', 'Price',
        #                               'TransactionDate'])
        # frames = [report, addon]
        # report = pd.concat(frames)

        merged = sample.merge(dumple, indicator=True, how='outer')
        match = pd.concat([match, merged], ignore_index=True)

sheets['Match'] = match
writer = pd.ExcelWriter('./report.xlsx', engine='xlsxwriter')

for sheet_name in sheets.keys():
    sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=None)

writer.save()

if __name__ == "__main__":

    def checking(sample, dumple):
        print("Совпадеине столбцов: " + str((dumple.columns.tolist()) == (sample.columns.tolist())))
        if len(sample.columns) == len(dumple.columns):
            return ("Количество столбцов совпадает.")
        elif len(sample.columns) < len(dumple.columns):
            return ("Количество столбцов больше.")
        else:
            return ("Количество столбцов меньше.")


    for file in os.listdir(files):
        if file.endswith(".csv"):
            path = files + file
            print(path)
            print('===============================================')
            dumple = pd.read_csv(path)
            print(checking(sample, dumple))
            print('===============================================')
