# -*- coding: utf-8 -*-
# 脚本名称: [serv00 web保活]
# 功能描述: [网页登录]
# 环境变量设置:
#   - 名称：[servCK]   格式：[username#password]
#   - 多账号处理方式：[暂不支持]
# 定时设置: [0 0 9 ? * 1]
# new Env("serv00保活")
import os
import sys
import requests
import mechanize
from html.parser import HTMLParser
import logging
from datetime import datetime
accounts = ''
class MyHTMLParser(HTMLParser):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.success = False

    def handle_data(self, data):
        if f'Zalogowany jako: {self.username}' in data:
            self.success = True

# Use os.path.expanduser to expand the path
log_file_path = os.path.expanduser('../files/serv00_web_login.log')

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)



# 创建一个浏览器对象
br = mechanize.Browser()
br.set_handle_robots(False)   # 忽略 robots.txt

# 设置 User-Agent 头部
br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36')]

# Flag to track overall success
all_successful = True

logging.info("开始尝试登录...")

# Iterate over each account
for account in accounts:
    logging.info(f"{account['name']}尝试登录")

    try:
        # Open the login page
        response = br.open(account['url'])

        # Select the login form
        br.select_form(nr=1)

        # Fill in the form
        br['username'] = account['username']
        br['password'] = account['password']

        # Submit the form
        response = br.submit()

        # Use the custom HTML parser to verify login success
        parser = MyHTMLParser(account['username'])
        parser.feed(response.read().decode())

        if parser.success:
            logging.info(f"{account['name']}登录成功")
        else:
            logging.error(f"{account['name']}登录失败")
            all_successful = False  # Set the flag to False if any login fails

    except Exception as e:
        logging.error(f"{account['name']}登录失败报错: {e}")
        all_successful = False  # Set the flag to False if an exception occurs

# Exit with 0 if all logins were successful, otherwise exit with 1
if all_successful:
    logging.info("Serv00网页登录成功")
    requests.get("这里可以放bark通知url")
    sys.exit(0)
else:
    logging.error("Serv00网页登录失败")
    requests.get("这里可以放bark通知url")
    sys.exit(1)
  

if __name__ == "__main__":
    env_name = 'servCK'
    token = os.getenv(env_name)
    if not token:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)

    cookies = re.split(r'[@\n]', token)
    print(f"共获取到{len(cookies)}个账号")
# List of accounts with their respective details
    accounts = [
    {'name': 'serv00', 'username': 'cookies.split("#")[0]', 'password': 'cookies.split("#")[1]', 'url': '你的web面板登录地址比如https://pane8.serv00.com/login/'}
]
    print(accounts)
