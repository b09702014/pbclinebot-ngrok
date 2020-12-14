from django.db import models

# Create your models here.
class User_Info(models.Model):
    uid = models.CharField(max_length=50,null=False,default='')         #user_id
    name = models.CharField(max_length=255,blank=True,null=False)       #LINE名字
    pic_url = models.CharField(max_length=255,null=False)               #大頭貼網址
    mtext = models.CharField(max_length=255,blank=True,null=False)      #文字訊息紀錄
    date = models.DateField(auto_now=True)                              #物件儲存的日期時間
    user_bmr = models.CharField(max_length=20,blank=True,null=False)    # 記錄使用者的BMR
    cal = models.CharField(max_length=20,blank=True,null=False)         # 記錄使用者還能吃的量
    data_type = models.CharField(max_length=20,blank=True,null=False)   # 記錄輸入資料類型
    food = models.CharField(max_length=20,blank=True,null=False)        # 記錄使用者吃了什麼
    period = models.CharField(max_length=20,blank=True,null=False)      # 記錄使用者進食的時段
    number = models.CharField(max_length=5,blank=True,null=False)       # 使用者的原始資料
    def __str__(self):
        return self.uid