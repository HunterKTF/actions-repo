'''
Boms Automation V1.0.0

Made by: Jorge R. Hernández Sabino
Updated: 06-17-21
Contact: jorgehernandez336@gmail.com
'''

import os
import time
import csv
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


# Function to retrieve file contents
def getFiles():
    pnp_files = []
    files = os.listdir()
    for x in files:
        if 'PnP' in x:
            pnp_files.append(x)
    return pnp_files

# Function to define users to share spreadsheet
def share_with():
    users = [
        'rhernandez@valiot.io'
    ]
    return users

# Function to get credentials to create a spreadsheet
def getCredentials():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/creds.json", scope)
    time.sleep(10)
    return gspread.authorize(creds)

def create_sheet():
    users = share_with()
    gc = getCredentials()
    files = getFiles()
    print(files)
    title = "test"
    sh = gc.create(title)
    sh.share(users, perm_type='user', role='writer')
    worksheet = sh.add_worksheet(title=title, rows="100", cols="20")
    time.sleep(10)
    return sh, worksheet

def create_titles(sh, worksheet):
    worksheet.update_cell(1,1,"Código Valiot")
    worksheet.update_cell(1,2,"Concepto")
    worksheet.update_cell(1,3,"Mouser Part Number")
    worksheet.update_cell(1,4,"Nombre")
    worksheet.update_cell(1,5,"Descripción")
    worksheet.update_cell(1,6,"Unidad")
    worksheet.update_cell(1,7,"Marca")
    worksheet.update_cell(1,8,"Enlace")
    worksheet.update_cell(1,9,"Cantidad")
    worksheet.update_cell(1,10,"Precio")
    worksheet.update_cell(1,11,"Subtotal")
    worksheet.update_cell(1,12,"Total")
    time.sleep(30)

def init_api():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    params = (
        ('apiKey', '2b5be052-2f7b-48e9-a36c-592d2ef8446b'),
    )
    time.sleep(10)
    return headers, params

os.chdir("/home/user/bin/CAM/")
csvFiles = getFiles()
dict_qty = {}
dict_val = {}
cc=0
for file in csvFiles:
    line_count=0
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            data_qty = row[4]
            if data_qty not in dict_qty and data_qty != ' ':
                dict_qty[data_qty]=1
                dict_val[data_qty]=row[0]
            elif data_qty != ' ':
                dict_qty[data_qty]+=1
                dict_val[data_qty]+=", "+row[0]

sh, worksheet = create_sheet()
ws = sh.sheet1
sh.del_worksheet(ws)
create_titles(sh, worksheet)
url = sh.url
url += "/edit#gid=0"
headers, params = init_api()
qString1 = '{ "SearchByPartRequest": { "mouserPartNumber": "'
qString2 = '", "partSearchOptions": "string" }}'
mpn = ''
time.sleep(10)

for key in dict_qty:
    if "@" in key:
        idx = key.find('@')
        length = len(key)
        value = key[idx+1:length]
        mpn = value.strip(' "')
        codigo_valiot = file[4:-9] + '-' + str(cc)
        qty = dict_qty[key]
        concept = "pruebas"
        parts = dict_val[key]
        mpn = value
        data = qString1 + mpn + qString2
        response = requests.post('https://api.mouser.com/api/v1/search/partnumber', headers=headers, params=params, data=data)
        q_url = response.json()
        worksheet.update_cell(cc+2,1,codigo_valiot)
        worksheet.update_cell(cc+2,2,concept)
        worksheet.update_cell(cc+2,3,mpn)
        worksheet.update_cell(cc+2,4,parts)
        worksheet.update_cell(cc+2,5,q_url["SearchResults"]["Parts"][0]["Description"])
        worksheet.update_cell(cc+2,6,1)
        worksheet.update_cell(cc+2,7,q_url["SearchResults"]["Parts"][0]["Manufacturer"])
        worksheet.update_cell(cc+2,8,q_url["SearchResults"]["Parts"][0]["ProductDetailUrl"])
        worksheet.update_cell(cc+2,9,qty)
        worksheet.update_cell(cc+2,10,q_url["SearchResults"]["Parts"][0]["PriceBreaks"][0]["Price"])
        worksheet.update_cell(cc+2,11,worksheet.cell(cc+2, 9, value_render_option='FORMULA').value * worksheet.cell(cc+2, 10, value_render_option='FORMULA').value)
        time.sleep(10)
        print(mpn)
        cc+=1

worksheet.update_cell(2,12,'=sum(K2:K' + str(cc+2) + ')')
print(url)
print("Hello World")
