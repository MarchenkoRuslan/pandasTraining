import pandas as pd
import os
from pandas.api.types import CategoricalDtype

files = 'files/'
match = pd.DataFrame()
sheets = {}

sample = pd.read_csv('sample_file.csv', converters={'AccountNumber': str})
report = pd.DataFrame([['sample_file.csv', len(sample.index), sample.shape[1]]
                       + [sample[col].dtype for col in list(sample)]],
                      columns=['File name', 'Row count', 'Col count'] + [col for col in list(sample)])
report['AccountNumber'] = str(report['AccountNumber'].values[0]) + '\n 8 digit'
report['SecurityCode'] = str(report['SecurityCode'].values[0]) + '\n choice of 3 values'
report['Price'] = str(report['Price'].values[0]) + '\n 0 digit after 0'
report['TransactionDate'] = str(report['TransactionDate'].values[0]) + '\n yyyy-mm-dd'

sheets['BASE'] = report

status_type = CategoricalDtype(categories=['EF', 'MF', 'OT'], ordered=False)
col_order = ['AccountNumber', 'SecurityCode', 'Price', 'TransactionDate']
data_types = {'AccountNumber': 'object',
              'SecurityCode': status_type,
              'Price': 'float64',
              'TransactionDate': 'object'}


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
            dumple = pd.read_csv(path, names=col_order, header=0, converters={'AccountNumber': str})
            dumple = dumple.loc[dumple['AccountNumber'] != "AccountNumber"]

    dumple = dumple.astype(data_types)
    return dumple


def sheet_generator(path):
    dumple = pd.read_csv(path, converters={'AccountNumber': str})

    sheets[file] = pd.DataFrame([[file, len(dumple.index), dumple.shape[1]]
                                 + [dumple[col].dtype for col in list(dumple)]],
                                columns=['File name', 'Row count', 'Col count'] + [col for col in list(dumple)])

    dumple = fix(sample, dumple)
    merged = sample.merge(dumple, indicator=True, how='outer')
    sheets['Match ' + file] = merged
    return sheets


sample = sample.astype(data_types)

for file in os.listdir(files):
    if file.endswith(".csv"):
        path = files + file
        sheet_generator(path)

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
            print(dumple)
            print(checking(sample, dumple))
            print('===============================================')
