# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         hykb.py
# @author           Echo
# @EditTime         2024/9/20
import os
import random
import re
import threading
import urllib.parse
from datetime import datetime

import httpx

from sendNotify import send_notification_message

if 'Hykb_cookie' in os.environ:
    Hykb_cookie = re.split("@", os.environ.get("Hykb_cookie"))
else:
    Hykb_cookie = []
    print("未查找到Hykb_cookie变量.")


class HaoYouKuaiBao():
    """好游快爆签到
    """

    def __init__(self, cookie):
        self.client = httpx.Client(
            verify=False,
            headers={
                "Origin": "https://huodong3.i3839.com",
                "Referer": "https://huodong3.3839.com/n/hykb/cornfarm/index.php?imm=0",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
        )
        self.cookie = cookie
        self.url = "https://huodong3.3839.com/n/hykb/{}/ajax{}.php"
        self.user_name = self.user_info()["user"]

    def get_index_html(self):
        """
        获取首页
        :return: 
        """
        url = "https://huodong3.3839.com/n/hykb/cornfarm/index.php?imm=0"
        try:
            response = self.client.get(url)
            return response.text
        except Exception as e:
            print("好游快爆-获取首页出现错误：{}".format(e))

    def user_info(self):
        """
        获取用户信息
        :return: 
        """
        url = self.url.format("qdjh", "")
        payload = f"ac=login&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
        try:
            response = self.client.post(url, content=payload).json()
            if response['key'] == 'ok':
                return {
                    "user": response["config"]["name"],
                    "uuid": response["config"]["uid"]
                }
        except Exception as e:
            print("好游快爆-获取用户信息出现错误：{}".format(e))

    def plant(self) -> int:
        """播种
        """
        url = self.url.format("cornfarm", "_plant")
        payload = f"ac=Plant&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
        try:
            response = self.client.post(url, content=payload).json()
            if response['key'] == 'ok':
                print(f"好游快爆-用户【{self.user_name}】播种成功")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                          f"好游快爆-用户【{self.user_name}】播种成功")
                return 1
            else:
                if response['seed'] == 0:
                    print(f"好游快爆-用户【{self.user_name}】种子已用完")
                    send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                              f"好游快爆-用户【{self.user_name}】种子已用完")
                    return -1
                else:
                    print(f"好游快爆-用户【{self.user_name}】播种失败")
                    send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                              f"好游快爆-用户【{self.user_name}】播种失败")
                    return 0
        except Exception as e:
            print(f"好游快爆-播种出现错误：{e}")
            return False

    def harvest(self) -> bool:
        """收获
        """
        url = self.url.format("cornfarm", "_plant")
        payload = f"ac=Harvest&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
        try:
            response = self.client.post(url, content=payload).json()
            if response['key'] == 'ok':
                print(f"好游快爆-用户【{self.user_name}】收获成功")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                          f"好游快爆-用户【{self.user_name}】收获成功")
            elif response['key'] == '503':
                print(f"好游快爆-用户【{self.user_name}】{response['info']}")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                          f"好游快爆-用户【{self.user_name}】{response['info']}")
            else:
                print(f"好游快爆-用户【{self.user_name}】收获失败")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                          f"好游快爆-用户【{self.user_name}】收获失败")
                return False
        except Exception as e:
            print(f"好游快爆-收获出现错误：{e}")
            return False

    def login(self):
        """登录
        """
        url = self.url.format("cornfarm", "")
        payload = f"ac=login&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
        response = self.client.post(url, content=payload)
        try:
            response = response.json()
            return response
        except Exception as e:
            print("好游快爆-登录出现错误：{}".format(e))

    def watering(self):
        """浇水
        """
        url = self.url.format("cornfarm", "_sign")
        payload = f"ac=Sign&verison=1.5.7.005&OpenAutoSign=&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"

        try:
            response = self.client.post(url, content=payload).json()
            if response['key'] == 'ok':
                print(f"好游快爆-用户【{self.user_name}】浇水成功")
                send_notification_message(title="好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                          content=f"好游快爆-用户【{self.user_name}】浇水成功")
                return 1, response['add_baomihua']
            elif response['key'] == '1001':
                print(f"好游快爆-用户【{self.user_name}】今日已浇水")
                send_notification_message(title="好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                          content=f"好游快爆-用户【{self.user_name}】今日已浇水")
                return 0, 0
            else:
                print("好游快爆-浇水出现错误：{}".format(response))
                return -1, 0
        except Exception as e:
            print("好游快爆-浇水出现错误：{}".format(e))
            return -1, 0

    def get_goods(self):
        """
        获取商品id
        :return: 
        """
        response = self.client.post(
            url="https://shop.3839.com/index.php?c=Index&a=initCard",
            content=f"pid=1660&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
        )
        try:
            j_response = response.json()
            if j_response['code'] == 200:
                return j_response['data']['store_id'], j_response['data']['product_name']
        except Exception as e:
            print("好游快爆-获取商品id出现错误：{}".format(e))

    def buy_seeds(self):
        """购买种子
        """
        # 获取种子商品id
        goods_id, goods_name = self.get_goods()
        l_response = self.client.post(
            url="https://huodong3.3839.com/n/hykb/bmhstore2/inc/virtual/ajaxVirtual.php",
            content=f"ac=checkExchange&gid={goods_id}&t={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}&r=0.{random.randint(100000000000000000, 899999999999999999)}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
        ).json()
        if l_response['key'] != "200" and l_response['msg'] != "验证通过":
            print("好游快爆-购买种子出现错误：{}".format(l_response))
            return False
        else:
            # 购买种子
            response = self.client.post(
                url="https://huodong3.3839.com/n/hykb/bmhstore2/inc/virtual/ajaxVirtual.php",
                content=f"ac=exchange&t={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}&r=0.{random.randint(100000000000000000, 899999999999999999)}&goodsid={goods_id}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
            )
            try:
                j_response = response.json()
                if j_response['key'] == 200:
                    print(f"好游快爆-用户【{self.user_name}】购买了【{goods_name}】，还剩下🍿爆米花{j_response['bmh']}个")
                    send_notification_message(title="好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
                                              content=f"好游快爆-用户【{self.user_name}】购买了【{goods_name}】，还剩下🍿爆米花{j_response['bmh']}个")
                    return True
                else:
                    print("好游快爆-购买种子失败：{}".format(j_response))
                    return False
            except Exception as e:
                print("好游快爆-购买种子出现错误：{}".format(e))
                return False

    def sgin(self):
        info = ""
        # 登录
        data = self.login()
        if data['key'] == 'ok':
            print(f"用户： 【{self.user_name}】登录成功！✅")
            if data['config']['csd_jdt'] == "100%":
                # 收获
                if self.harvest():
                    info = info + "收获成功\n"
                    # 播种
                    b = self.plant()
                    if b == -1:
                        info = info + "播种失败，没有种子\n"
                    elif b == 1:
                        info = info + "播种成功\n"
                        # 浇水
                        data = self.watering()
                        if data[0] == 1:
                            info = info + f"浇水成功,获得{data[1]}爆米花\n"
                        elif data[0] == 0:
                            info = info + f"今日已浇水\n"
                        else:
                            info = info + f"浇水失败\n"
                    else:
                        info = info + "播种失败\n"
                else:
                    info = info + "收获失败\n"

            elif data['config']['grew'] == '-1':
                # 播种
                b = self.plant()
                if b == -1:
                    info = info + "播种失败，没有种子\n"
                elif b == 1:
                    info = info + "播种成功\n"
                    # 浇水
                    data = self.watering()
                    if data[0] == 1:
                        info = info + f"浇水成功,获得{data[1]}爆米花\n"
                    elif data[0] == 0:
                        info = info + f"今日已浇水\n"
                    else:
                        info = info + f"浇水失败\n"
                else:
                    info = info + "播种失败\n"

            else:
                # 浇水
                data = self.watering()
                if data[0] == 1:
                    info = info + f"浇水成功,获得{data[1]}爆米花\n"
                elif data[0] == 0:
                    info = info + f"今日已浇水\n"
                else:
                    info = info + f"浇水失败\n"
        else:
            info = info + "登录失败\n"

        return info


if __name__ == '__main__':
    threads = []
    for cookie_ in Hykb_cookie:
        hykb = HaoYouKuaiBao(cookie_)
        thread = threading.Thread(target=hykb.sgin)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
