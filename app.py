from flask import Flask, jsonify, request
import os
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
#    a=os.environ['Authorization']
    return "Test Line Bot"

@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        return "OK"

@app.route('/callback', methods=['POST'])
def callback():
  json_line = request.get_json()
  json_line = json.dumps(json_line)
  decoded = json.loads(json_line)
  user = decoded["events"][0]['replyToken']
  #id=[d['replyToken'] for d in user][0]
  #print(json_line)
  print("ผู้ใช้：",user)
  sendText(user,'งง') # ส่งข้อความ งง
  return '',200

def sendText(user, text):
  LINE_API = 'https://api.line.me/v2/bot/message/reply'
  Authorization = 'Bearer ' + os.environ['Authorization'] # ตั้ง Config vars ใน heroku พร้อมค่า Access token
  headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': Authorization
  }
  data = json.dumps({
    "replyToken":user,
    "messages":[{"type":"text","text":text}]
  })
  r = requests.post(LINE_API, headers=headers, data=data) # ส่งข้อมูล

if __name__ == '__main__':
    app.run()
