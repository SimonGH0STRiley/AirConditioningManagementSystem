# Frontend Development Server
- server (server端代码，包括websocket和resfulapi)
- frontendDevServer (django 服务器配置项)

# 运行
## 安装环境
pip install -r requirements.txt
## 初始化数据库
pip manage.py makemigrations
pip manage.py migrate

## 运行服务器
pip mamage.py runserver [ip:port]

ps: 运行websocket服务需要先运行redis并将端口映射至6379
