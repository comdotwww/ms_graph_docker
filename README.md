# ms_graph_docker
 use E5 graph apis

# 使用方法
## 安装 docker compose
> 先安装curl：`sudo apt install -y curl ` 或  `sudo yum install -y curl`

```bash
# 国内
bash <(curl -sSL https://gitee.com/SuperManito/LinuxMirrors/raw/main/DockerInstallation.sh)
```

```bash
# 国际
bash <(curl -sSL https://raw.githubusercontent.com/SuperManito/LinuxMirrors/main/DockerInstallation.sh)
```

## 创建容器
```shell
mkdir -p /opt/ms_graph_docker/
cd /opt/ms_graph_docker/
wget https://fastly.jsdelivr.net/gh/comdotwww/ms_graph_docker@latest/docker-compose.yml
docker rm -f ms_graph_docker
docker compose pull
```
然后根据自己需要编辑`docker-compose.yml`里的`environment`内容，其中：
```
TZ: "Asia/Shanghai" # 必填，默认"Asia/Shanghai"
TG_BOT_TOKEN: "" # 选填 telegram bot token，可通过 t.me/botfather 获取
TG_SEND_ID: "11111"  # 选填，如填写，则TG_BOT_TOKEN也要填写 telegram bot 主人的id 需要先给 bot 发一条消息
CLIENT_ID: "client_id" # 必填
CLIENT_SECRET: "client_secret" # 必填
TOKEN_FIRST: "" #必填
PROXY_URL: "null"  # 选填 代理 url ，如反向代理地址 http://example.com/ 则填写 example.com 设置方法 https://www.hostloc.com/thread-805441-1-1.html
```
可以先手动执行一次，看看是否成功
```
cd /opt/ms_graph_docker/
docker compose up -d
```
查看日志，看看是否成功
```
docker logs -f ms_graph_docker
```

## 周期执行
编辑 cron 周期执行表达式，如：
```
0 3,4,5 * * 1-5  cd /opt/ms_graph_docker/;docker compose up -d
```
意思是：从星期一到星期五，每周的第 3、4 和 5 小时后的第 0 分钟执行

# 配置信息获取
1. 前往 https://portal.azure.com/ 登陆管理员账号。（[这里](https://portal.azure.com/#settings)可以把语言改成中文）。
![](https://pic.rmb.bdstatic.com/bjh/02d71730c6d3127bad103dd7c88c83da.png)
2. 首页找到`Azure Active Directory`（如果没有可以搜索或者点击[这里](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview)）然后点击[应用注册](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps)-> +新注册
![](https://pic.rmb.bdstatic.com/bjh/01e0c00051e1c9f1d7d21ea512c0c7ea.png)
3. `名称`随便填写，`受支持的账户类型`选择`任何组织目录(任何 Azure AD 目录 - 多租户)中的帐户`，`重定向URI`填写：`http://localhost:53682/`。
![](https://pic.rmb.bdstatic.com/bjh/a97d9c17cc21038cf4fd6410210a21aa.png)
4. 注册成功后，将`应用程序(客户端)ID`记录下来，后面会用到！
![](https://pic.rmb.bdstatic.com/bjh/05c91736bd458252d4fad1d67b3f2ff3.png)
5. 点击左侧菜单`API权限` -> `添加权限` -> `Microsoft Graph`-> 选中`委托的权限`。以下权限分别搜索勾选！勾选完点击按钮`添加权限`。
![](https://pic.rmb.bdstatic.com/bjh/1b1cb013b6b7477a1b4c409a24c45379.png)
6. 在API权限页面，如果界面上有`代表xxx授予管理员同意`按钮，一定要点一下，然后同意授权！如果没有这个按钮，就不用管了！
![](https://pic.rmb.bdstatic.com/bjh/846189e6a636dc4f300a814696621d05.png)
![](https://pic.rmb.bdstatic.com/bjh/e3469d880e4f0c5fb60426bc7cda1f83.png)
7. 点击左侧菜单`证书和密码`-> `+新客户端密码`,`说明`随便填，`截止期限`选最长的！点击`添加`按钮。然后页面下方可见新建的密码，然后将`值`复制记录下来！后面会用到！
![](https://pic.rmb.bdstatic.com/bjh/384eaf1a8e2c21d490fa271af05e57ba.png)
![](https://pic.rmb.bdstatic.com/bjh/0eca14a52583c92c011379164a807e49.png)
8. 利用rclone来获取 Token。以 Windows 为例：
Windows下载rclone（[rclone下载地址](https://rclone.org/downloads/)）到电脑某个盘符下，在rclone.exe同目录中，按Shift+鼠标右键，选择在【此处打开cmd窗口】或【在此处打开powershell窗口】
![](https://pic.rmb.bdstatic.com/bjh/88caaf99e0140e0891e01d4e4fc37f0d.png)
然后在弹出的窗口执行命令！(根据第4步和第7步的结果)
```
rclone.exe authorize "onedrive" "应用程序(客户端)ID" "应用程序密码"
```
执行命令后弹出网页登陆管理账号，然后接受授权即可！
![](https://pic.rmb.bdstatic.com/bjh/dca231f1fd57293961ccab7a16d42d21.png)
授权成功后，窗口弹出得到的Token信息！复制内容。仅复制 【Paste the following into your remote machine --->】开头【<---End paste】结尾的中间部分内容！
![](https://pic.rmb.bdstatic.com/bjh/020571d9071e1aaa9778ef7de0179c79.png)
用这个[在线转化工具](https://c.runoob.com/front-end/53/)，提取`refresh_token`的值。
![](https://i.imgur.com/oygCGXd.png)

9. 最后填入配置信息