from django.contrib import admin

# Register your models here.
from 聊天機器人.models import *

class User_Info_Admin(admin.ModelAdmin):
    list_display = ('uid','name','data_type','mtext','food','period','date','user_bmr','cal','number')
admin.site.register(User_Info,User_Info_Admin)