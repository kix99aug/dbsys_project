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
# 這邊是Linebot的授權TOKEN(等等註冊LineDeveloper帳號會取得)，我們為DEMO方便暫時存在settings裡面存取，實際上使用的時候記得設成環境變數，不要公開在程式碼裡喔！
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


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

        for event in events:
            if isinstance(event, MessageEvent):
                url = 'http://localhost:8000/api/search'
                str_list = []
                output = ""
                d = {"value": event.message.text}
                r = requests.post(url, data=d)
                data = r.json()
                if len(data['result']) != 0:
                    count = 1
                    for i in data['result']:
                        string = "第" + str(count) + "項商品 :" + i['model'] + '\n'
                        if (len(output)+len(string) < 2000):
                            output += string
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=output)
                            )
                            output = string
                        count = count + 1
                    line_bot_api.reply_message(
                        event.reply_token,
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
