from django.shortcuts import render
from django.http import HttpResponse

import sys
import os

import gspread
from fast_bitrix24 import Bitrix


webhook = "https://altair.bitrix24.ua/rest/1/pq4jor2ovao54xbi/"
b = Bitrix(webhook)

gc = gspread.service_account(filename=os.path.abspath('GoogleSheet/creds.json'))

def AddOrderSheet(*args, **kwargs):
    sh = gc.open("Orders")
    sheet = sh.sheet1

    order_id = [*args][0]
    cell = sheet.find(str(order_id))
    
    if cell == None:
        sheet.append_row([*args])
    

def UpdateOrderSheet(order_id, *args, **kwargs):
    sh = gc.open("Orders")
    update_arr=[*args][0]


    worksheet = sh.sheet1

    cell = worksheet.find(str(order_id))

    if cell:
        row = cell.row
        col = cell.col


        for key in update_arr:
            value = update_arr[key]
            worksheet.update(key+str(row), value)

def NewOrder(order_id):
    deal = b.get_all(
        'crm.deal.list',
        params={
            'select': ['*', 'UF_*'],
            'filter': {'ID': str(order_id)}
    })[0]


    contact = b.get_all(
        'crm.contact.list',
        params={
            'select': ['Name', 'PHONE', "*"],
            'filter': {'ID': deal["CONTACT_ID"]}
    })[0]

    order_id = deal["ID"]
    order_date = str(deal["BEGINDATE"].split("T")[0])
    order_status = "На отправку"
    order_prepayment = deal["UF_CRM_1633275701280"]
    order_sum = deal["OPPORTUNITY"]
    order_discount = 0
    order_count = deal["UF_CRM_1649747064818"][0]
    order_adress = deal["UF_CRM_1633274704683"]
    order_phone = contact["PHONE"][0]["VALUE"]
    order_holdername = contact["NAME"]
    order_ttn = deal["UF_CRM_1645092420180"]

    if deal["UF_CRM_1650966063918"] == '45':
        order_item = "Бронежелет MARK IV"

    print(order_date)
    
    AddOrderSheet(
        order_id,
        order_date,
        order_status,
        order_prepayment,
        order_sum,
        order_discount,
        order_count,
        order_item,
        order_adress,
        order_phone,
        order_holdername,
        order_ttn)

def index(request):
    try:
        order_id = request.GET["order_id"]

        try:
            NewOrder(order_id)
            return HttpResponse("200")
        except:
            return HttpResponse("Invalid order_id status 400")
    except:
        return HttpResponse("Invalid order_id status 400")