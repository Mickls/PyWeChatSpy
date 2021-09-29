import redis

# from rpc_client_tools import RPCProxy
#
# spy = RPCProxy()
REDIS_IP = "81.68.222.63"
REDIS_PASSWORD = "TowCat"
redis_client = redis.Redis(host=REDIS_IP, password=REDIS_PASSWORD, port=6379, db=0, decode_responses=True)

WECHAT_API = "http://47.98.182.74:21119/MyWeChatHTTPAPI"

XIAOICE_PHONE = 18202865067
XIAOICE_PASSWORD = "ppnn13%dkst2.1"

XIAOICE_LOGIN_URL = "https://login.xiaoice.com/SignIn/PasswordLoginForSlideVerify"
XIAOICE_SEND_MESSAGE_URL = "https://ux-plus.xiaoice.com/s_api/game/getresponse?workflow=AIBeingsGFChat"
XIAOICE_CROSS_SITE_COLLECTOR_URL = "https://ux-plus.msxiaobing.com/CrossSiteCollector"
XIAOICE_GET_BATCH_URL = "https://ux-plus.xiaoice.com/d_api/aibeingsexternalmark/get_batch"
