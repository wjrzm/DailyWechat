from datetime import datetime, timedelta
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os
import random
import json

nowtime = datetime.utcnow() + timedelta(hours=8)
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d")

# 如果你想部署在GitHub Actions上，可以使用下面的代码
# app_id = os.getenv("APP_ID")
# app_secret = os.getenv("APP_SECRET")
# template_id = os.getenv("TEMPLATE_ID")

# 如果你想部署在GitLab上，可以使用下面的代码
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"
template_id = "YOUR_TEMPLATE_ID"
weatherApiKey = "YOUR_WEATHER_API_KEY"


def get_time():
    dictDate = {'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三', 'Thursday': '星期四',
                'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期天'}
    a = dictDate[nowtime.strftime('%A')]
    return nowtime.strftime("%Y年%m月%d日 %H时%M分 ") + a


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# 天气API使用https://dev.qweather.com/的API


def get_geo(district, city):
    urlGeo = "https://geoapi.qweather.com/v2/city/lookup?location=" + \
        district + "&adm=" + city + "&key=" + weatherApiKey
    location = requests.get(urlGeo).json()
    return location["location"][0]["id"]


def get_weather(district, city):
    urlWeather = "https://devapi.qweather.com/v7/weather/3d?location=" + \
        get_geo(district, city) + "&key=" + weatherApiKey
    weather = requests.get(urlWeather).json()

    return weather["daily"][0]


def get_air(district, city):
    urlAir = "https://devapi.qweather.com/v7/air/now?location=" + \
        get_geo(district, city) + "&key=" + weatherApiKey
    air = requests.get(urlAir).json()

    return air["now"]


def get_count(born_date):
    delta = today - datetime.strptime(born_date, "%Y-%m-%d")
    return delta.days + 1


def get_leftday(setday):
    nextdate = datetime.strptime(str(today.year) + "-" + setday, "%Y-%m-%d")
    if nextdate < today:
        nextdate = nextdate.replace(year=nextdate.year + 1)
    return (nextdate - today).days


if __name__ == '__main__':
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)

    f = open("./users_info.json", encoding="utf-8")
    js_text = json.load(f)
    f.close()
    data = js_text['data']
    num = 0
    for user_info in data:
        born_date = user_info['born_date']
        birthday = user_info['birthday'][5:]
        setday = user_info['setday'][5:]
        city = user_info['city']
        district = user_info['district']
        user_id = user_info['user_id']
        # name=user_info['user_name'].upper()

        weather = get_weather(district, city)
        air = get_air(district, city)

        data = dict()
        data['time'] = {
            'value': get_time(),
            'color': '#470024'
        }
        data['words'] = {
            'value': get_words(),
            'color': get_random_color()
        }
        data['weather'] = {
            'value': weather['textDay'],
            'color': '#002fa4'
        }
        data['city'] = {
            'value': city,
            'color': get_random_color()
        }
        data['tem_high'] = {
            'value': weather['tempMax'],
            'color': '#D44848'
        }
        data['tem_low'] = {
            'value': weather['tempMin'],
            'color': '#01847F'
        }
        data['born_days'] = {
            'value': get_count(born_date),
            'color': get_random_color()
        }
        data['birthday_left'] = {
            'value': get_leftday(birthday),
            'color': get_random_color()
        }
        data['setday_left'] = {
            'value': get_leftday(setday),
            'color': get_random_color()
        }
        data['air'] = {
            'value': air['category'],
            # 'value': "good",
            'color': get_random_color()
        }
        data['wind'] = {
            'value': weather['windDirDay'],
            'color': get_random_color()
        }
        # data['name'] = {
        #     'value': name,
        #     'color': get_random_color()
        #     }
        data['uv'] = {
            'value': weather['uvIndex'],
            'color': get_random_color()
        }

        res = wm.send_template(user_id, template_id, data)
        print(res)
        num += 1
    print("已发送", num, "条消息")
