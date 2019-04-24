from oauth2client.service_account import ServiceAccountCredentials
import gspread
import numpy as np


def enter_size(filename, sheetname, mouseno, width, length, date):
    # enforce all inputs are strings
    # if not isinstance(filename, str)

    # authenticate and read google spreadsheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'C:/Users/wade/Downloads/Tumor Entry-16400702de93.json', scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(filename).worksheet(sheetname)

    # # find cell to update
    # column_headers = np.array(worksheet.row_values(1))
    # if np.where(column_headers == date)[0].size > 0:
    #     myCol = np.where(column_headers == date)[0][0]
    # else:
    #     myCol = len(column_headers)
    #     print(myCol)
    #     worksheet.update_cell(1, myCol+1, date)
    #     worksheet.update_cell(1, myCol+2, date)
    #     worksheet.update_cell(1, myCol+3, date)
    # row_headers = np.array(worksheet.col_values(1))
    # if np.where(row_headers == mouseno)[0].size == 1:
    #     myRow = np.where(row_headers == mouseno)[0] + 1
    # else:
    #     print('Error. Either mouse ' + mouseno + ' does not exist or there are duplicate entries')
    #
    # # update
    # worksheet.update_cell(myRow, myCol+1, width)
    # worksheet.update_cell(myRow, myCol+2, length)
    # worksheet.update_cell(myRow, myCol+3, float(width)*float(length))

    # update v2
    cell_list = worksheet.range('A1:B2')
    print(cell_list)
    worksheet.update_cells(cell_list)


enter_size('wz_10', 'Sheet14', '5', '3.51', '4.52', '2019-06-11')
