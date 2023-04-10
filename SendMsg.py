import os
from fake_useragent import UserAgent
import requests as req

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_SEND_ID = os.getenv('TG_SEND_ID')


class SendMessage:
    # 发送 TG Bot 消息
    def send_tg_msg(msg):
        if not TG_BOT_TOKEN or not TG_SEND_ID:
            print("TG_BOT_TOKEN 或者 TG_SEND_ID 不存在")
            return
        PROXY_URL = os.getenv('PROXY_URL')
        if not PROXY_URL or PROXY_URL.lower() == "null":
            PROXY_URL = "api.telegram.org"
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': UserAgent().random
            }
            if req.get(r'https://' + PROXY_URL + r'/bot' + TG_BOT_TOKEN + r'/sendMessage?chat_id=' + TG_SEND_ID + r'&text=' + msg, headers=headers).status_code == 200:
                print('发送 TG Bot 消息 成功')
        except:
            print("发送 TG Bot 消息 失败")
            pass
