import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
from datetime import date
import locale

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('C_PATH'), scope)
gc = gspread.authorize(credentials)
sheet_name = 'test-mika' # 共有したシートならなんでも可能

try:
    wks = gc.open(sheet_name) #操作するシートを指定する
except gspread.exceptions.SpreadsheetNotFound:
    print('そのシートは存在しません')
    sys.exit()

sheet_key = wks.id
month = date.today().month
day = date.today().day
title = f'{month}/{day}'

"""
workbook: １つのスプレッドシートファイル
worksheet: スプレッドシートファイルのタブ
"""

#keyでworkbook取得 -> keyじゃないとコピーとかできないらしい
wb = gc.open_by_key(sheet_key)
worksheet_list = list(map(lambda x:x.title, wb.worksheets()))
template_sheet = wb.get_worksheet(0)

#正しく機能させるために1,2,3が抜けていた場合はエラーを吐くように入力フォームを注意する必要あり

# 出力する行番号を取得
def get_output_row(worksheet):
    row_count = 5 # 入力は5行目から
    # 学籍番号, 氏名, 当日の体温が入力されているか判定
    while worksheet.cell(row_count,2).value != "" or worksheet.cell(row_count,3).value != "" or worksheet.cell(row_count,4).value != "":
        row_count += 1
    return row_count

#新規sheet作成
if title not in worksheet_list:
    wb.duplicate_sheet(source_sheet_id = template_sheet.id, new_sheet_name = title, insert_sheet_index=1) # templateから新しいsheetを追加

    # 活動日の情報
    year = date.today().year
    nengo = year-2018
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    day_of_the_week = date(year, month, day).strftime('%a')

    info = [['課外活動団体名     ネットボール部','','','','',f'活動日:令和{nengo}年{month}月{day}日({day_of_the_week})']]

    info_range = f'{title}!A3'
    wb.values_update(
        info_range,
        params={'valueInputOption': 'RAW'},
        body={'values': info}
    )

latest_sheet = wb.get_worksheet(1)
last_row = get_output_row(latest_sheet)

#入力
student_number = 'a'
name = 'b'
temp = 'c'

my_list = [[student_number, name, temp]]
sheet_range = f'{title}!B{last_row}'
wb.values_update(
    sheet_range,
    params={'valueInputOption': 'RAW'},
    body={'values': my_list}
)



