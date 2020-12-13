from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#models.py資料表
from 聊天機器人.models import *

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        message=[]

        """
        message.append(TextSendMessage(text=str(body)))
        """

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name

                if ',' in mtext:  # BMR計算(性別,體重,身高,年齡)
                    try:
                        data = mtext.split(",")
                        if data[0] == "m":  # 男生
                            cal = (13.7*float(data[1])) + (5.0*float(data[2])) - (6.8*float(data[3])) + 66
                            BMR = str(cal)
                        elif data[0] == "f":  # 女生
                            cal = (9.6*float(data[1])) + (1.8*float(data[2])) - (4.7*float(data[3])) + 655
                            BMR = str(cal)
                        else:
                            BMR = "你的輸入格式怪怪的歐"
                    except:
                            BMR = "你的輸入格式怪怪的歐"

                    if BMR != "你的輸入格式怪怪的歐":
                        message.append(TextSendMessage(text=("你的BMR值:" + BMR)))
                        if User_Info.objects.filter(uid=uid).exists()==False:
                            User_Info.objects.create(uid=uid,name=name,data_type="個人資料",mtext=mtext,user_bmr=BMR,cal=BMR)
                            message.append(TextSendMessage(text='個人資料新增完畢'))
                        elif User_Info.objects.filter(uid=uid).exists()==True:
                            message.append(TextSendMessage(text='已修改個人資料囉'))
                            User_Info.objects.filter(uid=uid).update(user_bmr=BMR,cal=BMR)
                    else:
                        message.append(TextSendMessage(text=BMR))
                elif "查詢資料" in mtext:
                    if User_Info.objects.filter(uid=uid).exists()==True:
                        infor = User_Info.objects.get(uid=uid,data_type="個人資料")

                        message.append(TextSendMessage(text="你的BMR值：" + infor.user_bmr))
                        message.append(TextSendMessage(text="你還能吃:" + infor.cal))
                    else:
                        message.append(TextSendMessage(text="你還沒輸入資料喔"))
                line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()