import csv
import openpyxl as excel
import os
import sys
from datetime import datetime
from glob import glob
from pprint import pprint


def read_csv(fname):
    with open(fname, mode='r', encoding='sjis') as f:
        reader = csv.reader(f)
        return [row for row in reader]


base_dir = os.path.dirname(__file__)
resouce_dir = base_dir + '/excel/'
template_file = resouce_dir + 'template.xlsx'
dt_today = datetime.now()
today= dt_today.strftime('%Y%m%d')
output_file = resouce_dir + 'output_' + today + '.xlsx'

file_dict = {'1_Sheet1': '1_*.csv',
            '2_Sheet2': '2_*.csv',
            }

book = excel.load_workbook(template_file)
for sheet in book.worksheets:
    try:
        glob_result = glob(resouce_dir + file_dict[sheet.title])
    except KeyError:
        continue
        
    if len(glob_result) > 1:
        print('対象ファイルが複数あります。読み込みデータを整理してください。')
        sys.exit()
    else:
        target = glob_result[0]
        
    for row_index, values in enumerate(read_csv(target)):
        for col_index, item in enumerate(values):
            # row: 1行目はヘッダ,2行目から書き込み
            # print(row_index + 2, col_index+1, item)
            sheet.cell(row=row_index+2, column=col_index+1, value=item)
book.save(output_file)
