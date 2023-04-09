# -*- coding: UTF-8 -*-
import requests as req
from fake_useragent import UserAgent
from SendMsg import SendMessage
import json
import os
import sys
import time
# 先注册azure应用,确保应用有以下权限:
# files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# 注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用
# redirect_uri 是 http://localhost:53682/


path = sys.path[0]+r'/token.txt'
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
token_first = os.getenv('TOKEN_FIRST')

# 获取token并写入


class Update:
    def gettoken(refresh_token):
        # client_id client_secret 不存在，跳过
        if not client_id or not client_secret:
            SendMessage.send_tg_msg(r"client_id client_secret 不存在，跳过")
            SendMessage.send_tg_msg(r"更新 token 失败")
            return

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'User-Agent': UserAgent().random
                   }
        data = {'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': 'http://localhost:53682/'
                }
        html = req.post(
            'https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
        jsontxt = json.loads(html.text)
        refresh_token = jsontxt['refresh_token']
        access_token = jsontxt['access_token']
        with open(path, 'w+') as f:
            f.write(refresh_token)
            f.close()

    def update_token():
        try:
            fo = open(path, "r+")
            refresh_token = fo.read()
            if len(refresh_token) < 5:
                refresh_token = token_first
            fo.close()
            gettoken(refresh_token)
            SendMessage.send_tg_msg(r"更新 token 成功")
        except:
            SendMessage.send_tg_msg(r"更新 token 失败")
            return


    if __name__ == '__main__':
        update_token()
