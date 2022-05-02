from django.shortcuts import render
from django.http import HttpResponse

from fast_bitrix24 import Bitrix

webhook = "https://altair.bitrix24.ua/rest/1/pq4jor2ovao54xbi/"
b = Bitrix(webhook)


def BitrixUpdate(deal_id, dict_value):
    method = 'crm.deal.update'
    params = {'ID': deal_id, 'fields': dict_value}
    return b.call(method, params)


def index(request):
    dict_value = request.GET

    if "order_id" in dict_value:
        order_id = dict_value["order_id"]
        fields_dict = {}

        for dict_key in dict_value:
            if dict_key != "order_id":
                fields_dict.update({dict_key:dict_value[dict_key]})
        
        if(BitrixUpdate(order_id, fields_dict)):
            return HttpResponse("200")
        else:
            return HttpResponse("Error 400 !")
    else:
        return HttpResponse("Invalid order_id !")