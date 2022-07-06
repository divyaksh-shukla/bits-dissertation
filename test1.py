from datetime import datetime, timedelta
import openpyxl
from os.path import splitext, join
import csv

def read_excel_file(excel_filename,sheetname):
    book = openpyxl.load_workbook(excel_filename, read_only=True)
    data_sheet = book[sheetname]

    return data_sheet

def get_data_cells(sheet,range_from, range_to):
    data_cells = sheet[range_from:range_to]
    return data_cells

def format_data(cells):
    data = list()
    current_datetime = datetime(2013,1,1,0,0,0)
    hour = 0
    for row in cells:
        for i, cell in enumerate(row):
            if (i == 0):
                continue
                # current_datetime = cell.value
                # if(not(type(current_datetime) is datetime)):
                #     print(type(current_datetime))
            else:
                data.append((current_datetime + timedelta(hours = hour), cell.value))
                hour += 1
    return data

def put_into_csv(data, csv_filename):
    csv_file = open(csv_filename, 'w')
    for d in data:
        csv_file.write(f'{d[0]},{d[1]}\n')
    csv_file.close()

def wth():
    new_data_book = openpyxl.Workbook()
    new_data_sheet = new_data_book.active
    
    for dest_row, source_row in zip(new_data_sheet['A1':'Y1827'], data_cells):
        for dest_cell, source_cell in zip(dest_row, source_row):
            dest_cell.value = source_cell.value
    # new_data_sheet.values = data_cells

    filename_wo_extension, extension = splitext(excel_filename)[0], splitext(excel_filename)[1]
    new_data_book.save(filename_wo_extension + '_data' + extension)
    print('done')
    

if __name__ == '__main__':
    sheet = read_excel_file(excel_filename='HandBookData.xlsx', sheetname='DPLLoad')
    data_cells = get_data_cells(sheet, 'D2', 'AB1827')
    data = format_data(data_cells)
    put_into_csv(data, 'HandBookData.csv')
