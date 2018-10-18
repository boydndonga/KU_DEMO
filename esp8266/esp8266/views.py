import json
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.conf import settings

from .esp8266_client import send_data


def show_buttons(request):
    return render(request,"index.html",{})



def toggle_button(request):
    d=json.loads(request.body)
    x={True:"1",False:"0"}
    s="{}{}".format(d["number"],x[d["state"]])
    send_data(settings.ESPADDR,settings.ESP_PORT,s)
    return JsonResponse({"success":"State changes"})