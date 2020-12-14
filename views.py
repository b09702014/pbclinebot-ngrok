from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

import datetime

#models.py資料表
from 聊天機器人.models import *

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        message=[]
        today = datetime.date.today()

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
                
                food_dict = {"滷肉飯":150, "珍珠奶茶":250}

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
                        if User_Info.objects.filter(uid=uid,data_type="個人資料",number=1).exists() == False:
                            User_Info.objects.create(uid=uid,name=name,data_type="個人資料",mtext=mtext,user_bmr=BMR,cal=BMR,number=1)
                            message.append(TextSendMessage(text='個人資料新增完畢'))
                        elif User_Info.objects.filter(uid=uid,data_type="個人資料",number=1).exists() == True:
                            message.append(TextSendMessage(text='已修改個人資料囉'))
                            User_Info.objects.filter(uid=uid,data_type="個人資料",number=1).update(user_bmr=BMR,cal=BMR)
                    else:
                        message.append(TextSendMessage(text=BMR))
                elif "查詢資料" in mtext:
                    if User_Info.objects.filter(uid=uid,data_type="個人資料",number=1).exists() == True:
                        infor = User_Info.objects.get(uid=uid,data_type="個人資料",number=1)  # number指的是原始資料

                        if User_Info.objects.filter(uid=uid,data_type="個人資料",date=today).exists() == False:
                            User_Info.objects.create(uid=uid,data_type="個人資料",name=name,user_bmr=infor.user_bmr,cal=infor.user_bmr)

                        user = User_Info.objects.get(uid=uid,data_type="個人資料",date=today)  # 當天的使用者紀錄
                        # print(user.data_type)
                        message.append(TextSendMessage(text="你的BMR值：" + user.user_bmr))
                        message.append(TextSendMessage(text="你今天還能吃:" + user.cal + "大卡"))
                    else:
                        message.append(TextSendMessage(text="你還沒輸入資料喔"))
                elif "+" in mtext:
                    try:
                        text_str = mtext.strip("+").split("/")
                        if text_str[1] in food_dict:
                            User_Info.objects.create(uid=uid,name=name,mtext=mtext,data_type="吃東西",food=text_str[1],period=text_str[0],cal=food_dict[text_str[1]])

                            if User_Info.objects.filter(uid=uid,data_type="個人資料",number=1).exists() == True:
                                infor = User_Info.objects.get(uid=uid,data_type="個人資料",number=1)  # number指的是原始資料
                            else:
                                message.append(TextSendMessage(text="你還沒輸入資料喔"))

                            if User_Info.objects.filter(uid=uid,data_type="個人資料",date=today).exists() == False:
                                User_Info.objects.create(uid=uid,data_type="個人資料",name=name,user_bmr=infor.user_bmr,cal=infor.user_bmr)
                            
                            user = User_Info.objects.get(uid=uid,data_type="個人資料",date=today)  # 當天的使用者紀錄
                            calculate = float(user.cal) - float(food_dict[text_str[1]])
                            User_Info.objects.filter(uid=uid,data_type="個人資料",date=today).update(cal=str(calculate))
                            

                            message.append(TextSendMessage(text=("您吃了:" + text_str[1] + ", " + "熱量為" + str(food_dict[text_str[1]]) + "大卡")))
                            message.append(TextSendMessage(text="資料已記錄完畢"))
                        else:
                            message.append(TextSendMessage(text="抱歉,我們沒有您輸入食物的熱量喔"))
                    except:
                        message.append(TextSendMessage(text="你的輸入格式怪怪的歐"))
                elif "歷史資料" in mtext:
                    push = TemplateSendMessage(
                                alt_text='好消息來囉～',
                                template=ButtonsTemplate(
                                thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
                                title="要查詢哪一天？",
                                text="選個日期吧",
                                    actions=[
                                        DatetimePickerTemplateAction(
                                            label="想看哪一天",
                                            data="gettime",
                                            mode="date",
                                            initial="2020-12-06",
                                            min="2011-06-23",
                                            max=str(today)
                                            )
                                        ]
                                )
                        )
                    message.append(push)

                #if User_Info.get(uid=uid,data_type="個人資料",date=today).exist() == True:
                #   print(User_Info.get(uid=uid,data_type="個人資料",date=today))
                #  print(User_Info.objects.all())
                line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, PostbackEvent):
                #mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name

                if ("-" in event.postback.params['date']):
                    check = event.postback.params['date']
                    message.append(TextSendMessage(text="您選的日期是:" + check))
                    #print(User_Info.objects.filter(data_type="個人資料",date=check).exists())
                    print(User_Info.objects.all())
                    #if User_Info.objects.filter(uid=uid,data_type="個人資料",date=check).exists() == True:
                     #   user_eat = User_Info.objects.get(uid=uid,data_type="個人資料",date=check)
                      #  print(user_eat)
                        #eat_cal = float(user_eat.user_bmr) - float(user_eat.cal)

                        #message.append(TextSendMessage(text="您在" + check + "總共吃了" + str(eat_cal) + "大卡"))   
                        
                line_bot_api.reply_message(event.reply_token,message)
                    #print(body)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()