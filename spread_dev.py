import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import date
import locale

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

title = 'test_day'
if title not in worksheet_list:
    #新規sheet作成
    wb.duplicate_sheet(source_sheet_id = form.id, new_sheet_name = title, insert_sheet_index=1)
    year = date.today().year
    nengo = year-2018
    dt = date(year, month, day)
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    day_of_the_week = dt.strftime('%a')
    info = [['課外活動団体名     ネットボール部','','','','',f'活動日:令和{nengo}年{month}月{day}日({day_of_the_week})']]

    info_range = f'{title}!A3'
    wb.values_update(
        info_range, 
        params={'valueInputOption': 'RAW'}, 
        body={'values': info}
    )

now = wb.get_worksheet(1)
last_row = detect_last_row(now)

#入力
student_number = 
name = 
temp = 

my_list = [[student_number, name, temp]]
Sheet_range = f'{title}!B{last_row}'
wb.values_update(
    Sheet_range, 
    params={'valueInputOption': 'RAW'}, 
    body={'values': my_list}
)


