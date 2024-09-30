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

    # def buy_seeds(self):
    #     """购买种子
    #     """
    #     # 获取种子商品id
    #     goods_id, goods_name = self.get_goods()
    #     print(goods_id, goods_name)
    #     headers = {
    #         # 'User-Agent': "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.104 Mobile Safari/537.36Androidkb/1.5.7.507(android;Redmi K30 Pro;12;1080x2356;WiFi);@4399_sykb_android_activity@",
    #         # 'Accept': "application/json, text/javascript, */*; q=0.01",
    #         # 'Accept-Encoding': "gzip, deflate",
    #         # 'X-Requested-With': "XMLHttpRequest",
    #         'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    #         'Origin': "https://huodong3.3839.com",
    #         # 'Sec-Fetch-Site': "same-origin",
    #         # 'Sec-Fetch-Mode': "cors",
    #         # 'Sec-Fetch-Dest': "empty",
    #         # 'Referer': "https://huodong3.3839.com/n/hykb/bmhstore2/inc/virtual/index.php?gid=14403&jtype=1",
    #         # 'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    #         # 'Cookie': "cornfarm_iback_v5=ok; Hm_lvt_f1fb60d2559a83c8fa1ee6125a352bd7=1726835084; HMACCOUNT=A31622759CFC8814; friend_iback_v5=ok; cornfarm_shop_v1=ok; Birthday_btn_v1=ok; UM_distinctid=1921fb977e97c-0d88697ab29ace-6c074671-53c31-1921fb977ea7e; cornfarm_moren_btn_v1=ok; Hm_lpvt_f1fb60d2559a83c8fa1ee6125a352bd7=1727595549"
    #     }
    #     url = "https://huodong3.3839.com/n/hykb/bmhstore2/inc/virtual/ajaxVirtual.php"
    #     # payload = f"ac=login&gid=14403&t=2024-09-29+15%3A39%3A33&r=0.4950858317265687&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
    #     payload = "ac=login&gid=14403&t=2024-09-29+15%3A39%3A33&r=0.4950858317265687&scookie=1%7C0%7C128421985%7C5b%2Br54iG55So5oi3MTI4NDIxOTg1%7CkbA25014349F11473F467DC6FF5C89E9D6%7CplcAoJ6jITDlGvEnGl80IlfuoREWIlVjITZOpv6U7WI%3D%251%7C5312899df0a922f9707df9a5ad8dee37&device=kbA25014349F11473F467DC6FF5C89E9D6"
    #     l_response = requests.post(
    #         url=url,
    #         headers=headers,
    #         data=payload,
    #         verify=False
    #         # content=f"ac=login&t={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}&r=0.{random.randint(100000000000000000, 899999999999999999)}&gid={goods_id}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
    #     ).json()
    #     if l_response['key'] != "ok":
    #         print("好游快爆-购买种子出现错误：{}".format(l_response))
    #         return False
    #     else:
    #         # 购买种子
    #         response = self.client.post(
    #             url="https://huodong3.3839.com/n/hykb/bmhstore2/inc/virtual/ajaxVirtual.php",
    #             content=f"ac=exchange&t={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}&r=0.{random.randint(100000000000000000, 899999999999999999)}&goodsid={goods_id}&scookie={urllib.parse.quote(self.cookie)}&device=kbA25014349F11473F467DC6FF5C89E9D6"
    #         )
    #         try:
    #             j_response = response.json()
    #             print(j_response)
    #             if j_response['key'] == 200:
    #                 print(f"好游快爆-用户【{self.user_name}】购买了【{goods_name}】")
    #                 send_notification_message(title="好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"),
    #                                           content=f"好游快爆-用户【{self.user_name}】购买了【{goods_name}】")
    #                 return True
    #             else:
    #                 print("好游快爆-购买种子失败：{}".format(j_response))
    #                 return False
    #         except Exception as e:
    #             print("好游快爆-购买种子出现错误：{}".format(e))
    #             return False

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
