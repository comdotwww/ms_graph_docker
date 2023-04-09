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
TG_SEND_ID: "11111"  # 选填，如填写，则TG_BOT_TOKEN也要填写 telegram bot 主人的id
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