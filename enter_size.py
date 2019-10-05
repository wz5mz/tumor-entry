#! /data/data/com.termux/files/usr/bin/env python3

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import numpy as np
import sys
import re

filename = sys.argv[1]
sheetname = sys.argv[2]
# width, length, mouseno = sys.argv[3].splitlines()
# date = re.search('\d\d\d\d-[0-1]\d-[0-3]\d', sys.argv[4]).group(0)
mouseno = re.search('\d+', sys.argv[3]).group(0)
width = float(re.search('(\d*\.\d+|\d+)', sys.argv[4]).group(0))
length = float(re.search('(\d*\.\d+|\d+)', sys.argv[5]).group(0))
date = re.search('\d\d\d\d-[0-1]\d-[0-3]\d', sys.argv[6]).group(0)


def enter_size(filename, sheetname, mouseno, width, length, date):
    # enforce all inputs are strings
    # if not isinstance(filename, str)

    # authenticate and read google spreadsheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/data/data/com.termux/files/home/storage/downloads/Tumor Entry-f14983e25cb2.json', scope)
#    credentials = ServiceAccountCredentials.from_json_keyfile_name(
#        'c:/users/wade/downloads/Tumor Entry-f14983e25cb2.json', scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(filename).worksheet(sheetname)

    # create list of cells to update [gspread.models.Cell]
    cell_list = []
    row_headers = np.array(worksheet.col_values(1))
    if np.where(row_headers == mouseno)[0].size == 1:
        myRow = np.where(row_headers == mouseno)[0][0] + 1
    else:
        print('Error. Either mouse ' + mouseno + ' does not exist or there are duplicate entries')
    column_headers = np.array(worksheet.row_values(1))
    if np.where(column_headers == date)[0].size > 0:
        myCol = np.where(column_headers == date)[0][0]
    else:
        myCol = len(column_headers)
        cell_list += [gspread.models.Cell(1, myCol+1, str(date)),
                      gspread.models.Cell(1, myCol+2, str(date)),
                      gspread.models.Cell(1, myCol+3, str(date))]
    cell_list += [gspread.models.Cell(myRow, myCol+1, width),
                  gspread.models.Cell(myRow, myCol+2, length),
                  gspread.models.Cell(myRow, myCol+3,
                                      float(width)*float(length))]

    # update - faster if only 1 call is made
    print(cell_list)
    if not worksheet.cell(myRow, myCol+1).value and not worksheet.cell(myRow, myCol+2).value and not worksheet.cell(myRow, myCol+3).value:
        worksheet.update_cells(cell_list)


enter_size(filename, sheetname, mouseno, width, length, date)
