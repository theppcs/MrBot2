from flask import Flask, jsonify, request, make_response
import os
import json
import numpy as np

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

lineaccesstoken = os.environ['Authorization']
line_bot_api = LineBotApi(lineaccesstoken)

####################### new ########################

@app.route('/')
def index():
    return "Test Line Bot"

@app.route("/webhook", methods=['POST'])
def webhook():
    question_from_dialogflow_raw = request.get_json(silent=True, force=True)

    answer_from_bot = generating_answer(question_from_dialogflow_raw)

    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json'
    return r

def generating_answer(question_from_dialogflow_dict):
    print(json.dumps(question_from_dialogflow_dict, indent=4, ensure_ascii=False))

    intent_group_question_str = question_from_dialogflow_dict["queryResult"]["intent"]["displayName"]

    if intent_group_question_str == 'LotteryRandom':
      answer_str = menurecommendation()
    elif intent_group_question_str == 'BMI - Confirmed W and H':
      answer_str = BMI_calculation(question_from_dialogflow_dict)
    else: answer_str = "หนูไม่รู้"

    answer_from_bot = {"fulfillmentText": answer_str}

    answer_from_bot = json.dumps(answer_from_bot, indent=4)
    print('answer_from_bot')
    print(answer_from_bot)

    return answer_from_bot

def menurecommendation():
    menu_name = '428358'
    answer_function = menu_name + ' สิ ถูกแน่นอน'
    return answer_function

def BMI_calculation(response_dict):
    print('response_dict')
    print(json.dumps(response_dict["queryResult"]["outputContexts"][1], indent=4, ensure_ascii=False))
    weight_kg = float(response_dict["queryResult"]["outputContexts"][1]["parameters"]["Weight.original"])    
    height_cm = float(response_dict["queryResult"]["outputContexts"][1]["parameters"]["Height.original"])    

    BMI = weight_kg / (height_cm/100)**2
    if BMI < 18.5 :
      answer_function = "คุณผอมเกินไปนะ"
    elif 18.5 <= BMI < 23.0 :
      answer_function = "คุณมีน้ำหนักปกติ"
    elif 23.0 <= BMI < 25.0 :
      answer_function = "คุณมีน้ำหนักเกิน"
    elif 25.0 <= BMI < 30.0 :
      answer_function = "คุณอ้วน"
    else :
      answer_function = "คุณอ้วนมาก"

    return answer_function

@app.route('/callback', methods=['POST'])
def callback():
  json_line = request.get_json()
  json_line = json.dumps(json_line)
  decoded = json.loads(json_line)
  no_event = len(decoded['events'])
  for i in range(no_event):
      event = decoded['events'][i]
      event_handle(event)
  return '',200

def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''

    if msgType == "text":
        msg = str(event["message"]["text"])
        replyObj = TextSendMessage(text=msg)
        line_bot_api.reply_message(rtoken, replyObj)

    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''

if __name__ == '__main__':
    app.run()
