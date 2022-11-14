#%%
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_date():
  weekday_num = date.today().weekday()
  if weekday_num == 0:
    today_date = str(date.today()) + '  星期一'
  elif weekday_num == 1:
    today_date = str(date.today()) + '  星期二'
  elif weekday_num == 2:
    today_date = str(date.today()) + '  星期三'
  elif weekday_num == 3:
    today_date = str(date.today()) + '  星期四'
  elif weekday_num == 4:
    today_date = str(date.today()) + '  星期五'
  elif weekday_num == 5:
    today_date = str(date.today()) + '  星期六'
  elif weekday_num == 6:
    today_date = str(date.today()) + '  星期日'
  return today_date

def get_reporter():
  reporters = ['厨师猪','小宝猪','企鹅仔','大企鹅包','噗噗','啾咪军团','树懒包包']
  return random.choice(reporters)

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"reporter":{'value':get_reporter(),'color':"#0000FF"},"today_date":{"value":get_date()},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count(),"color":"#FFC0CB"},"birthday_left":{"value":get_birthday(),"color":"#1E90FF"},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

# %%
