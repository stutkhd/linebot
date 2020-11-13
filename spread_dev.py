import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import date

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('C_PATH'), scope)
gc = gspread.authorize(credentials)
sheet_name = 'test'
wks = gc.open(sheet_name) #操作するスプシを指定する
sheet_key = wks.id
month = date.today().month
day = date.today().day
title = f'{month}/{day}'

#keyでworkbook取得 -> keyじゃないとコピーとかできないらしい
wb = gc.open_by_key(sheet_key)
worksheet_list = list(map(lambda x:x.title, wb.worksheets()))

form = wb.get_worksheet(0)
if len(worksheet_list) > 1:
    ws1 = wb.get_worksheet(1) #一番最新の検温記録
    ws1_title = ws1.title

#正しく機能させるために1,2,3が抜けていた場合はエラーを吐くように入力フォームを注意する必要あり
def detect_last_row(worksheet):
    row_count = 5
    while worksheet.cell(row_count,2).value != "" or worksheet.cell(row_count,3).value != "" or worksheet.cell(row_count,4).value != "":
        row_count += 1
    return row_count

if title not in worksheet_list:
    #新規sheet作成
    wb.duplicate_sheet(source_sheet_id = form.id, new_sheet_name = title, insert_sheet_index=1)

now = ws.get_worksheet(2)
#最後の行を取得
last_row = detect_last_row(now)
