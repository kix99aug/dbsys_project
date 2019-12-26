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
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

import time
# 這邊是Linebot的授權TOKEN(等等註冊LineDeveloper帳號會取得)，我們為DEMO方便暫時存在settings裡面存取，實際上使用的時候記得設成環境變數，不要公開在程式碼裡喔！
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

user_stage = {
    'id': {
        'stage': 0,
        'time': 123,
        'search': "apple",
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
        for event in events:  # 每個訊息進來時
            if isinstance(event, MessageEvent):
                if event.source.user_id in user_stage:
                    if time.time()-user_stage[event.source.user_id]['time'] <= 86400:
                        if user_stage[event.source.user_id]['stage'] == 1:
                            idx = int(event.message.text)-1
                            data = user_stage[event.source.user_id]['data']['result'][idx]['data']
                            columns = []
                            for i in range(len(data)):
                                print(i)
                                columns.append(CarouselColumn(thumbnail_image_url=data[i]['image_url'], title=data[i]['title'], text='$'+str(
                                    data[i]['price']), actions=[URITemplateAction(label='前往購買', uri=data[i]['url'])]))
                            line_bot_api.push_message(
                                event.source.user_id,
                                TemplateSendMessage(
                                    alt_text="請在手機上看唷", template=CarouselTemplate(columns=columns))
                            )
                            return HttpResponse()
                user_stage[event.source.user_id] = {
                    'stage': 1,
                    'time': time.time(),
                    'value': ()
                }
                url = 'http://localhost:8000/api/search'
                output = ""
                r = requests.post(url, data={"value": event.message.text})
                data = r.json()
                user_stage[event.source.user_id]['data'] = data
                if len(data['result']) != 0:
                    count = 1
                    for i in data['result']:
                        string = str(count) + " :" + i['model'] + '\n'
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
