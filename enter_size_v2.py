#! /data/data/com.termux/files/usr/bin/env python3

from oauth2client.service_account import ServiceAccountCredentials
import pygsheets
import numpy as np
import sys
import re
import time

filename = sys.argv[1]
sheetname = sys.argv[2]
mouseno = re.search('\d+', sys.argv[3]).group(0)
measurements = [re.search('(\d*\.\d+|\d+)', i).group(0) for i in sys.argv[4].split(',')]
date = re.search('\d\d\d\d-[0-1]\d-[0-3]\d', sys.argv[5]).group(0)

def enter_size_v2(filename, sheetname, mouseno, measurements, date):
    # authenticate and read google spreadsheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    gc = pygsheets.authorize(service_file='/data/data/com.termux/files/home/storage/downloads/Tumor Entry-f14983e25cb2.json')
#    gc = pygsheets.authorize(service_file='c:/users/wade/downloads/Tumor Entry-f14983e25cb2.json')
    sheet = gc.open(filename)
    worksheet = sheet.worksheet_by_title(sheetname)
    cell_list = []
    # find the row to enter user input
    row_headers = np.array([i[0] for i in worksheet.get_values(start=(1,1), end=(worksheet.rows,1), returnas='matrix')])
    myRow = int(np.where(row_headers == mouseno)[0][0] + 1)
    print(myRow)
    # find the col to enter user input
    column_headers = worksheet.get_values(start=(1,1), end=(1,worksheet.cols), returnas='matrix')[0]
    while column_headers[-1] == '':
        column_headers.pop()
    column_headers = np.array(column_headers)
    if np.where(column_headers == date)[0].size > 0:
        myCol = int(np.where(column_headers == date)[0][0])
    else:
        myCol = int(len(column_headers))
        cell_list += [pygsheets.Cell((1, myCol+1), str(date)),
                      pygsheets.Cell((1, myCol+2), str(date)),
                      pygsheets.Cell((1, myCol+3), str(date))]

    area_cell = pygsheets.Cell((myRow, myCol+3))
    myformula = measurements[0]+'*'+measurements[1]
    for i in range(2,len(measurements),2):
        myformula += '+'+measurements[i]+'*'+measurements[i+1]
    area_cell.formula = myformula
    cell_list += [pygsheets.Cell((myRow, myCol+1), measurements[0]),
                  pygsheets.Cell((myRow, myCol+2), measurements[1]),
                  area_cell]
    print(myCol)
    print(cell_list)

    if not worksheet.cell((myRow, myCol+1)).value and not worksheet.cell((myRow, myCol+2)).value and not worksheet.cell((myRow, myCol+3)).value:
        worksheet.update_cells(cell_list)

if len(measurements) % 2 == 0 and len(measurements) > 1:
   enter_size_v2(filename, sheetname, mouseno, measurements, date)

time.sleep(3)
