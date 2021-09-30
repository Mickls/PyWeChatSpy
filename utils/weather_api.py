import random

import requests
import json

KEY = 'SVeEqWVIMuml_t0Tc'  # API key(私钥)
UID = ""  # 用户ID, 当前并没有使用这个值,签名验证方式将使用到这个值

LOCATION = 'beijing'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
API = 'https://api.seniverse.com/v3/weather/daily.json'  # API URL，可替换为其他 URL
UNIT = 'c'  # 单位
LANGUAGE = 'zh-Hans'  # 查询结果的返回语言


nice_weather = [0, 1, 2, 3, 4, 5, 6]
normal_weather = [7, 8, 9]
rain_weather = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
snowy_weather = [20, 21, 22, 23, 24, 25]
dust_weather = [26, 27, 28, 29]
greasy_weather = [30, 31]
wind_weather = [32, 33, 34, 35, 36]


def fetch_weather(location, start=0, days=15):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT,
        'start': start,
        'days': days
    }, timeout=2)
    return result.json()


def get_weather_by_day(location, day=1):
    result = fetch_weather(location)
    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["daily"][day]
    }

    return normal_result


def get_care_text(code):
    if code in nice_weather:
        text_list = [
            "是个好天气呢ヾ(๑╹◡╹)ﾉ！",
            "要出去郊游吗。今天天气好好",
            "带二猫出去踏青怎么样",
            "故事的小黄花，从出生那年就飘着♪"
        ]
        # text = "是个好天气呢ヾ(๑╹◡╹)ﾉ！"
    elif code in normal_weather:
        text_list = [
            "天气很一般呢喵(●—●)",
            "至少今天不会很热，而且不会下雨(￣▽￣)~*"
        ]
        # text = "天气很一般呢喵(●—●)"
    elif code in rain_weather:
        text_list = [
            "要下雨啦，快回家收衣服o(ﾟДﾟ)っ！",
            "会下雨所以要记得带伞哦喵(*･ω< )",
            "雨一直下~~~你听过这首歌吗？好悲伤的说，二猫也不喜欢雨天",
            "要和二猫一起出去踩水玩吗？二猫有一双漂亮的雨靴"
        ]
    elif code in snowy_weather:
        text_list = [
            "二猫最喜欢雪啦！(*´ﾟ∀ﾟ｀)ﾉ ",
            "快带二猫出去堆雪人，二猫要堆一个超大的雪人",
            "雪天也要带伞哟，因为雪落在身上会化成水的⊙﹏⊙别问二猫为什么知道"
        ]
    elif code in dust_weather:
        text_list = [
            "咳咳咳，会有沙尘，所以出门要记得戴口罩哦(´･ω･)ﾉ(._.`)",
        ]
    elif code in greasy_weather:
        text_list = [
            "会有雾霾，出门一定要戴好口罩哦~",
            "大雾开车一定要小心，二猫等你安全回家(*･ω< )",
            "嗷呜，据说大雾里面都有怪兽，不听话的孩都要被吃掉"
        ]
    elif code in wind_weather:
        text_list = [
            "大风吹啊吹啊吹，你知道为什么会有风吗",
        ]
    else:
        text_list = [""]
    text = random.choice(text_list)
    return text


def get_weather(location, content):
    date, day = get_date(content)
    result = get_weather_by_day(location, date)

    text = "{}{}({})的天气情况为:\n白天: {}{}\n夜晚: {}{}\n气温: {}℃-{}℃"
    care_day = get_care_text(int(result['result']['code_day']))
    # care_night = get_care_text(int(result['result']['code_night']))
    text_message = text.format(
        result['location']['name'],
        day,
        result['result']['date'],
        result['result']['text_day'],
        f"({care_day})" if care_day else "",
        result['result']['text_night'],
        "",
        # f"({care_night})" if care_day else "",
        result['result']["low"],
        result['result']["high"],
    )
    return text_message


def get_date(text):
    if "今天" in text:
        return 1, "今天"
    elif "明天" in text:
        return 2, "明天"
    elif "后天" in text:
        return 3, "后天"
    else:
        return 1, "今天"


if __name__ == '__main__':
    print(get_weather("武汉", "@二猫 武汉今天天气"))
