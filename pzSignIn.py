# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         pzSignIn.py
# @author           Echo
# @EditTime         2024/9/13
import os
import re
from datetime import datetime

import httpx

if 'pz_account' in os.environ:
    pz_account = re.split("@|&", os.environ.get("pz_account"))
    print(f"查找到{len(pz_account)}个账号")
else:
    pz_account = []
    print("未查找到pz_account变量.")


def send_notification_message(title, content):
    try:
        from sendNotify import dingding_bot
        dingding_bot(title, content)
    except Exception as e:
        if e:
            print("发送通知消息失败")


class PzSignIn:
    def __init__(self, account):
        self.client = httpx.Client(base_url="https://service.ipzan.com", verify=False)
        self.get_token(account)

    def get_token(self, account):
        try:
            response = self.client.post(
                '/users-login',
                json={
                    "account": account,
                    "source": "ipzan-home-one"
                }
            )
            response_json = response.json()
        except Exception as e:
            print(e)
            print(response.text)
        token = response_json["data"]
        if token is not None:
            print("=" * 30 + f"登录成功，开始执行签到" + "=" * 30)
            self.client.headers["Authorization"] = "Bearer " + token
        else:
            print("登录失败")
            exit()

    def get_balance(self):
        """
        获取品赞余额
        :return: 
        """
        response = self.client.get(
            "/home/userWallet-find"
        ).json()
        return response["data"]["balance"]

    def sign_in(self):
        """
        品赞签到
        :return: 
        """
        response = self.client.get(
            "/home/userWallet-receive"
        ).json()
        if response["status"] == 200 and response['data'] == '领取成功':
            print("签到成功")
            print("=" * 100)
            balance = self.get_balance()
            send_notification_message(title="品赞代理签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                      content="签到成功，当前账户余额： " + balance)
        elif response["code"] == -1:
            balance = self.get_balance()
            print(response["message"])
            send_notification_message(title="品赞代理签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                      content=f"签到失败，{response['message']}\n当前账户余额：{balance}")
        else:
            print("签到失败！")
            print(response)


if __name__ == '__main__':
    for i in pz_account:
        pz = PzSignIn(i)
        pz.sign_in()
        del pz
