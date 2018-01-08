import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('JSON_FILE_PROVIDED_BY_GOOGLE', scope)

gc = gspread.authorize(credentials)

#Opening the fb_messenger_bot Sheet1
worksheet = gc.open("SHEET_NAME").sheet1

#returns the value within that cell
#val = worksheet.acell('B1').value # With label
#if the cell is empty, it would return ""

#Helpful Source
#http://gspread.readthedocs.io/en/latest/oauth2.html

