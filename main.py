import requests, json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from functools import reduce

from mqtt.subscribe import subscribe

realData = {
  "openfind1": -1,
  "openfind2": -1
}
name2Id = {
  "會議室1": "openfind1",
  "會議室2": "openfind2"

}
app = Flask(__name__)

def on_message(client, userdata, msg):
  global realData
  realData[msg.topic] = int(json.loads(msg.payload)["count"])

subscribe(on_message)

# params = {'access_token': 'rxc1SitGNuKaI05F0HzbnzdKpk0V5I2bfUvBOkxr7AFaOMxGAGjEqlMS8jBZv6QW'}
# headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json',
#             'Cookie': 'key=$AD820FA84E9A1341.allen_lin@openfind.com.tw:allen_lin@openfind.com.tw:mail.office.openfind.com.tw:tw'
#           }
# payload = {"roomId" : "6368c1606655b600d0f0a055", "text" : "炸 MM bug"}
# resp = requests.post(
#   'https://im.office.openfind.com.tw/api/messages',
#   params=params,
#   headers=headers,
#   data=json.dumps(payload)
# )
# 
# if not resp.status_code == requests.codes.ok:
#   print("error")
# print(resp.text)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('Xc2Ui6jPpHVp/orCMScKkasA570xU879/OesMq4lEGersiKpn1mVovJwn0HKZUdTMhup60m7eqfpTWUoZBiRqPz6ecWHSN4ynFjIFk9UTnUtgIxNnEGhXlEIaCR8iuGLX1GLau3Sa+bynDrS9kSQbgdB04t89/1O/w1cDnyilFU=')
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
def command(event):
  if event.message.text.startswith("rooms") or event.message.text.startswith("list"):
    params = str.split(event.message.text)[1:]
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=rooms(params))
    )
  elif event.message.text.startswith("check"):
    params = str.split(event.message.text)[1:]
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=check(params[0]))
    )
  elif event.message.text.startswith("notify"):
    params = str.split(event.message.text)[1:]
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=notify(params[0]))
    )
  else:
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text="default")
    )

def rooms(params):
  def core_all(v):
    return "．"+v
  def core_free(prev, curr):
    if ( realData[name2Id[curr]] <= 0 ):
      curr = "．" + curr 
      prev.append(curr)
    return prev

  if "free" in params:
    return "\n".join(list(reduce(core_free, name2Id.keys(), [])))
  return "\n".join(list(map(core_all, list(name2Id.keys()))))

def notify(roomName=None):
  if roomName == None:
    return "請輸入會議室名稱"

  params = {'access_token': 'rxc1SitGNuKaI05F0HzbnzdKpk0V5I2bfUvBOkxr7AFaOMxGAGjEqlMS8jBZv6QW'}
  headers = {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Cookie': 'key=$AD820FA84E9A1341.allen_lin@openfind.com.tw:allen_lin@openfind.com.tw:mail.office.openfind.com.tw:tw'
            }
  payload = {"roomId" : "6368c1606655b600d0f0a055", "text" : f"{roomName}現在可以使用囉!"}
  resp = requests.post(
    'https://im.office.openfind.com.tw/api/messages',
    params=params,
    headers=headers,
    data=json.dumps(payload)
  )
  
  if not resp.status_code == requests.codes.ok:
    return "MM通知發送失敗"
  return "MM通知發送成功"

def check(roomName=None):
  if roomName == None:
    return "請輸入會議室名稱"
  return f'{roomName}現在{"有人" if realData[name2Id[roomName]] > 0 else "沒有人"}喔'

if __name__ == "__main__":
  app.run()