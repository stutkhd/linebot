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
#シートの一覧
worksheet_list = list(map(lambda x:x.title, wb.worksheets()))

# #1番左は何も書いていないフォーマットにする
form = wb.get_worksheet(0) #コピーするsheet
if len(worksheet_list) > 1:
    ws1 = wb.get_worksheet(1) #一番最新の検温記録
    ws1_title = ws1.title

#すでにファイルが存在する
if title in worksheet_list:
    #userが入力を行う
    
else:
    #ファイルをコピーする
    wb.duplicate_sheet(source_sheet_id = form.id, new_sheet_name = title, insert_sheet_index=1)

