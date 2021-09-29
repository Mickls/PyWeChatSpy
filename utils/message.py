import re

from configs.settings import redis_client
from games.lottery import random_sign
from utils.chat_api import get_xiaoice_response


def message_processing(spy, from_wx, from_group_member, content):
    if from_wx == "gh_ab0072172f2d":
        match = re.search("<url><!\[CDATA\[https://.*\]\]></url>", content)
        if match:
            init_url = content[match.start() + 14: match.end() - 9]
            redis_client.set("xiaoice_init_url", init_url)
            redis_client.set("init_url_status", 1)
        return
    if "二猫抽签" in content:
        text = random_sign()
    else:
        text = get_xiaoice_response(content)
    spy.send_text(from_wx, text)
