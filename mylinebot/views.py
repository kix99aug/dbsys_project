import requests
from .models import *
from django.db import connection
from django.shortcuts import render

# Create your views here.
# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
#import datetime.sys
# 這邊是Linebot的授權TOKEN(等等註冊LineDeveloper帳號會取得)，我們為DEMO方便暫時存在settings裡面存取，實際上使用的時候記得設成環境變數，不要公開在程式碼裡喔！
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

user_stage = {
    'id': {
        'stage': 0,
        'time': 123,
        'search':"apple", 
    },
    'id': {
        'stage': 0,
        'time': 123
    }
}


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:    #每個訊息進來時
            if isinstance(event, MessageEvent):    
                if event.source.user_id in user_stage:   
                    for i in user_stage:    #如果之前傳過 先找到他在哪
                        if i == event.source.user_id:
                            index = i[event.source.user_id]
                            # todate = str(datetime.datetime.utcnow().strftime("%m%d"))
                            # if index['time'] == todate:    #如果時間是今天
                            # if index['stage'] ==1:    #且stage等於1
                            url = 'http://localhost:8000/api/search'
                            str_list = []
                            output = ""
                            d = {"value": index['search']}
                            r = requests.post(url, data=d)
                            data = r.json()
                            if len(data['result']) != 0:
                                j = data['result'][event.message.text]
                                for k in j['data']:
                                    string = k['title'] +'\n' + k['price'] + '\n' + k['url'] + '\n'
                                    if (len(output)+len(string) < 700):
                                        output += string
                                    else:
                                        line_bot_api.push_message(
                                            event.source.user_id,
                                            TextSendMessage(text=output)
                                        )
                                        output = string
                                    count = count + 1
                                line_bot_api.push_message(
                                    event.source.user_id,
                                    TextSendMessage(text=output)
                                )
                                del user_stage[event.source.user_id]
                                    
                            # else:    #如果不是今天
                            #     myid = event.source.user_id
                            #     vvalue = {}
                            #     vvalue['stage']:1
                            #     vvalue['time']:str(datetime.datetime.utcnow().strftime("%m%d"))
                            #     vvalue['search']:event.message.text
                            #     user_stage[event.source.user_id]:vvalue
                            #     url = 'http://localhost:8000/api/search'
                            #     str_list = []
                            #     output = ""
                            #     d = {"value": event.message.text}
                            #     r = requests.post(url, data=d)
                            #     data = r.json()
                            #     if len(data['result']) != 0:
                            #         count = 1
                            #         for j in data['result']:
                            #             string = str(count) +" :" + j['model'] + '\n'
                            #             if (len(output)+len(string) < 500):
                            #                 output += string
                            #             else:
                            #                 line_bot_api.push_message(
                            #                     event.source.user_id,
                            #                     TextSendMessage(text=output)
                            #                 )
                            #                 output = string
                            #             count = count + 1
                            #         line_bot_api.push_message(
                            #             event.source.user_id,
                            #             TextSendMessage(text=output)
                            #         )
                        else: 
                            continue
                else:
                    myid = event.source.user_id
                    vvalue = {}
                    vvalue['stage']:1
                    # vvalue['time']:str(datetime.datetime.utcnow().strftime("%m%d"))
                    user_stage[myid]:vvalue
                    url = 'http://localhost:8000/api/search'
                    str_list = []
                    output = ""
                    d = {"value": event.message.text}
                    r = requests.post(url, data=d)
                    data = r.json()
                    if len(data['result']) != 0:
                        count = 1
                        for i in data['result']:
                            string = str(count) +" :" + i['model'] + '\n'
                            if (len(output)+len(string) < 500):
                                output += string
                            else:
                                line_bot_api.push_message(
                                    event.source.user_id,
                                    TextSendMessage(text=output)
                                )
                                output = string
                            count = count + 1
                        line_bot_api.push_message(
                            event.source.user_id,
                            TextSendMessage(text=output)
                        )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# @csrf_exempt
# def callback(request):

#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')

#         try:
#             events = parser.parse(body, signature)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()

#         for event in events:
#             if isinstance(event, MessageEvent):

#                 line_bot_api.reply_message(
#                     event.reply_token,
#                     TextSendMessage(text=event.message.text)
#                 )
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()
