# -*- coding: UTF-8 -*-
import requests as req
import json
import sys
import time
import random
import os
from fake_useragent import UserAgent
from SendMsg import SendMessage
from update import Update
# 先注册azure应用,确保应用有以下权限:
# files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# 注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用
# redirect_uri 是 http://localhost:53682/

path = sys.path[0]+r'/token.txt'
num1 = 0
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
is_api_urls_extend = os.getenv('IS_API_URLS_EXTEND')


def gettoken(refresh_token):
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
    return access_token


def use_api():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    global num1
    access_token = gettoken(refresh_token)
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json',
        'User-Agent': UserAgent().random
    }
    print(r'此次运行开始时间为: ', time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()))
    SendMessage.send_tg_msg(
        r'此次运行开始时间为: ' + time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()))

    # API Requests
    base_graph_url = r'https://graph.microsoft.com/v1.0'
    graph_api_urls = [
        r'/me',
        r'/me/messages',
        r'/me/memberOf',
        r'/groups',
        r'/me/drive',
        r'/me/drive/items/root',
        r'/me/drive/root',
        r'/me/drive/root/children',
        r'/me/drive/sharedWithMe',
        r'/drive/root',
        r'/users',
        r'/me/mailFolders/inbox/messageRules',
        r'/me/mailFolders/inbox/messageRules',
        r'/me/drive/root/children',
        r'/me/mailFolders',
        r'/me/outlook/masterCategories',
    ]

    # 下面的 api 按需授权
    # graph
    graph_api_urls_extend = [
        base_graph_url + r'/me/calendars',  # Calendars.Read
        base_graph_url + r'/me/contacts',  # Contacts.Read
    ]
    other_api_urls_extend = [

    ]

    for url in graph_api_urls:
        try:
            if req.get(base_graph_url + url, headers=headers).status_code == 200:
                num1 += 1
                print(r"调用成功" + str(num1) + r'次')
                SendMessage.send_tg_msg(r'调用成功: ' + str(num1) + r' 次')
                time.sleep(random.randint(5, 10))
            else:
                print(time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()) +
                      "\n" + r"！！！状态码不是 200 ，api 是 " + base_graph_url + url + r' ！！！')
                SendMessage.send_tg_msg(
                    time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()
                                  ) + "\n" + r"！！！状态码不是 200 ，api 是 "
                    + base_graph_url + url + r' ！！！')
                time.sleep(random.randint(5, 10))
        except Exception as e:
            print(r"！！！调用接口失败，api 是 " + base_graph_url + url + r' ！！！')
            print(e.args)
            SendMessage.send_tg_msg(
                r"！！！调用失败，api 是 " + base_graph_url + url + r' ！！！')
            SendMessage.send_tg_msg(e.args)
            time.sleep(random.randint(5, 10))

    # 补充API
    if is_api_urls_extend.lower() == "true":
        print(r"调用补充 API 地址 开始")
        SendMessage.send_tg_msg(r"调用补充 API 地址 开始")
        for url in graph_api_urls_extend + other_api_urls_extend:
            try:
                if req.get(url, headers=headers).status_code == 200:
                    num1 += 1
                    print(r"调用成功" + str(num1) + r'次')
                    SendMessage.send_tg_msg(r'调用成功: ' + str(num1) + r' 次')
                    time.sleep(random.randint(5, 10))
                else:
                    print(time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()
                                        ) + "\n" + r"！！！状态码不是 200 ，api 是 " + url + r' ！！！')
                    SendMessage.send_tg_msg(
                        time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime()) + "\n" + r"！！！状态码不是 200 ，api 是 " + url + r' ！！！')
                    time.sleep(random.randint(5, 10))

            except Exception as e:
                print(r"！！！调用接口失败，api 是 " + url + r' ！！！')
                print(e.args)
                SendMessage.send_tg_msg(r"！！！调用失败，api 是 " + url + r' ！！！')
                SendMessage.send_tg_msg(e.args)
                time.sleep(random.randint(5, 10))
        print(r"调用补充 API 地址 结束")
        SendMessage.send_tg_msg(r"调用补充 API 地址 结束")

# 计算调用耗时
def format_time(time_diff):
    if time_diff < 60:
        return "耗时%.0f秒" % time_diff
    elif time_diff < 3600:
        minutes, seconds = divmod(time_diff, 60)
        return "耗时%d分%.0f秒" % (minutes, seconds)
    else:
        hours, seconds = divmod(time_diff, 3600)
        minutes, seconds = divmod(seconds, 60)
        return "耗时%d小时%d分%.0f秒" % (hours, minutes, seconds)


if __name__ == '__main__':
    start_time = time.time()

    print(time.strftime(r"%Y-%m-%d %H:%M:%S",
          time.localtime()) + r" Microsoft API 应用 开始")
    SendMessage.send_tg_msg(time.strftime(
        r"%Y-%m-%d %H:%M:%S", time.localtime()) + r"Microsoft API 应用 开始")

    Update.update_token()
    cycle_count = random.randint(10, 20)
    for i in range(cycle_count):
        print(r"第" + str(i + 1) + r"次循环")
        SendMessage.send_tg_msg(r"第" + str(i + 1) + r"次循环")
        use_api()
        time.sleep(random.randint(30, 60))

    print(time.strftime(r"%Y-%m-%d %H:%M:%S",
          time.localtime()) + r" Microsoft API 应用 结束")
    SendMessage.send_tg_msg(time.strftime(
        r"%Y-%m-%d %H:%M:%S", time.localtime()) + r"Microsoft API 应用 结束")
    
    end_time = time.time()
    time_diff = end_time - start_time
    format_time_str = format_time(time_diff)
    print(format_time_str)
    SendMessage.send_tg_msg(format_time_str)
