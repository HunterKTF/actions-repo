'''

'''

# Import dependencies
import requests
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time
import os

def getDir():
    path = '/home/user/bin/CAM/Assembly/optoSensor.csv'
    title = path[path.rfind("/")+1:-4]
    return path, title

def share_with():
    users = [
        'rhernandez@valiot.io',
        'jorgehernandez336@gmail.com',
        'jorge.hernandezs@gmail.com'
    ]
    return users

def getCredentials():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    time.sleep(10)
    return gspread.authorize(creds)

def create_sheet():
    users = share_with()
    gc = getCredentials()
    path, title = getDir()
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
    time.sleep(30)

def update_sheet():
    gc = getCredentials()
    path, title = getDir()
    sh = gc.open(title).sheet1
    return sh

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

def main():
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
    path, title = getDir()
    time.sleep(10)

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        cc = 0
        for row in csv_reader:
            codigo_valiot = title + '-' + str(cc)
            qty = row[0]
            line = row[1]
            parts = row[4]
            concept = "pruebas"
            if '@' in line:
                idx = line.find('@')
                length = len(line)
                value = line[idx+1:length]
                mpn = value.strip(' "')
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
                cc += 1
            line_count += 1
        worksheet.update_cell(2,12,'=sum(K2:K' + str(cc+2) + ')')
    print(url)
    # sed ' 1 s/.*/&123/' yourfile.txt

main()
