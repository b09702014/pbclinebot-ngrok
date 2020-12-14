#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

import json
from flask import Flask, request, abort
from linebot import (
LineBotApi, WebhookHandler
)
from linebot.exceptions import (
InvalidSignatureError
)
from linebot.models import (
MessageEvent, TextMessage, TextSendMessage,
)
app = Flask(__name__)
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
@app.route("/callback", methods=['POST'])
def callback():
# get X-Line-Signature header value
signature = request.headers['X-Line-Signature']
# get request body as text
body = request.get_data(as_text=True)
app.logger.info("Request body: " + body)
# handle webhook body
try:
handler.handle(body, signature)
except InvalidSignatureError:
abort(400)
return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
# get user id when reply
user_id = event.source.user_id

line_bot_api.reply_message(
event.reply_token,
TextSendMessage(text=event.message.text))
@app.route('/')
def homepage():
return 'Hello, World!'
if __name__ == "__main__":
app.run()

CHANNEL_ACCESS_TOKEN = "MggKcDsZV0s35ghPMPr57AojPLUMORyStOL3GymFcy2k50aXPwKhXqhnQyX5X7Zga7QfMyOo/I8JEHm3mpqWpwl6kOmYgV3468EORwpKGdDcXxjJTEcyH0NtBOPZqTldhSBDxA4MjwkRgpUUy5fRzAdB04t89/1O/w1cDnyilFU="

to = user_id

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

#文字訊息

try:
    line_bot_api.push_message(to, TextSendMessage(text='你今天記錄熱量了嗎？'))
except LineBotApiError as e:
    # error handle
    raise e