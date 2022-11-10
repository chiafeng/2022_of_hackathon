from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('oAjo17ATPcJM0hs3P4eGtOuIhfmlw8a6RO67R0a5SEPpRNQRRi1Z4e1L7wVPWhvRMhup60m7eqfpTWUoZBiRqPz6ecWHSN4ynFjIFk9UTnXjqXckngITPyBaZ9hldFNmw0nlBwjRNpWDEDVaTadJzwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d0ae03272e21774632be78e4a25163f2')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']

  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError: 
    abort(400)

  return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text)
  )

if __name__ == "__main__":
  app.run()