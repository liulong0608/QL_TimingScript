# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         hykb_tasks.py
# @author           Echo
# @EditTime         2024/9/24
import asyncio
import os
import random
import re
import urllib.parse
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from fn_print import fn_print
from sendNotify import send_notification_message_collection


if 'Hykb_cookie' in os.environ:
    hykb_cookie = re.split("@", os.environ.get("Hykb_cookie"))
    print(f"查找到{len(hykb_cookie)}个账号")
else:
    hykb_cookie = []
    print("未查找到Hykb_cookie变量.")
    exit()


class AsyncHykbTasks:
    def __init__(self, cookie):
        self.client = httpx.AsyncClient(base_url="https://huodong3.3839.com",
                                        headers={
                                            'User-Agent': "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.104 Mobile Safari/537.36Androidkb/1.5.7.507(android;Redmi K30 Pro;12;1080x2356;WiFi);@4399_sykb_android_activity@",
                                            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                                            'Origin': "https://huodong3.3839.com",
                                            'Referer': "https://huodong3.3839.com/n/hykb/newsign/index.php?imm=0",
                                        },
                                        verify=False)
        self.cookie = cookie
        self.temp_id = []
        self.bmh_tasks = []
        self.items = []

    async def get_task_ids(self):
        response = await self.client.get("/n/hykb/qdjh/index.php")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        list_items = soup.select(".game-list-item")
        for item in list_items:
            btn = item.select_one(".item-time")
            if btn and "已结束" not in btn.get("onclick", "") and "hd_id" in btn["onclick"]:
                onclick = btn["onclick"].replace("每日签到领", "")
                parts = onclick.split("'")
                self.items.append({
                    "title": parts[3],
                    "id": re.search(r"hd_id=(.+)", parts[1]).group(1)
                })

    async def get_bmh_task_ids(self):
        """
        获取爆米花相关任务的id
        :return: 
        """
        response = await self.client.get("/n/hykb/cornfarm/index.php?imm=0")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        task_list = soup.select(".taskDailyUl > li")
        for task_item in task_list:
            tasks_infos = task_item.select_one("dl")
            id_param = tasks_infos.select_one("dd")["class"][0]
            title_param = tasks_infos.select_one("dt").get_text()
            reward_param = tasks_infos.select_one("dd").get_text()
            self.bmh_tasks.append(
                {
                    "bmh_task_id": re.search(r"daily_dd_(.+)", id_param).group(1),
                    "bmh_task_title": re.search(r"分享福利：(.*)", title_param).group(1),
                    "reward_num": re.search(r"可得+(.+)", reward_param).group(1)
                }
            )

    async def get_task(self, a, hd_id_):
        try:
            payload = f"ac={a}&hd_id={hd_id_}&hd_id2={hd_id_}&t={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}&r=0.{random.randint(1000000000000000, 8999999999999999)}&scookie={self.cookie}"
            url = "https://huodong3.3839.com/n/hykb/newsign/ajax.php"
            self.client.headers["Referer"] = f"https://huodong3.3839.com/n/hykb/newsign/index.php?imm=0&hd_id={hd_id_}"
            response = await self.client.post(
                url=url,
                data=payload,
            )
            response_json = response.json()
            return response_json
        except Exception as e:
            print(e)
            return None

    async def process_item(self, item, bmh_itme):
        id = item["id"]
        await self.get_task("login", id)
        data = await self.get_task("signToday", id)

        await self.do_tasks_every_day(bmh_itme)
        await self.get_task_reward(bmh_itme)

        key = str(data["key"])
        if key == "-1005":
            fn_print("体验游戏中,请一分钟后再刷新领取☑️")
            await self.get_task("tiyan", id)
            # self.temp_id.append(
            #     {
            #         "title": item["title"],
            #         "id": id
            #     }
            # )  # 将正在体验的活动id加入列表中
        elif key == "-1007":
            await self.get_task("sharelimit", id)
            fn_print(f"活动【{item['title']}】分享成功！✅")
            await self.get_task("login", id)
            await self.get_task("signToday", id)
        elif key == "-1002":
            fn_print(f"活动【{item['title']}】奖励已领取过了！")
        elif key == "200":
            fn_print(f"活动【{item['title']}】签到成功！✅已签到{data['signnum']}天")
        elif key == "no_login":
            fn_print("⚠️⚠️scookie失效,请重新配置⚠️⚠️")
            return False
        return True

    async def do_tasks_every_day(self, task_items: dict):
        """
        调度每日必做任务
        :return: 
        """
        # 分享任务
        share_url = "https://huodong3.3839.com/n/hykb/cornfarm/ajax_daily.php"
        share_data = {
            "ac": "DailyShareCallback",
            "id": "{}".format(task_items["bmh_task_id"]),
            "mode": "qq",
            "source": "ds",
            "r": f"0.{random.randint(100000000000000, 8999999999999999)}",
            "scookie": self.cookie,
            "device": "kbA25014349F11473F467DC6FF5C89E9D6"
        }
        share_response = await self.client.post(url=share_url, json=share_data)
        try:
            share_response_json = share_response.json()
            if share_response_json["key"] == "ok" and share_response_json["info"] == "可以领奖":
                fn_print("任务: {}, 可以领奖了.".format(task_items["bmh_task_title"]))
                return True
            else:
                fn_print("任务: {}, 不可以领奖".format(task_items["bmh_task_title"]))
                return False
        except Exception as e:
            fn_print("调度任务异常：", e)
            fn_print(share_response.text)

    async def get_task_reward(self, task_items: dict):
        """
        领取任务奖励
        :param task_items: 任务组
        :return: 
        """
        url = "https://huodong3.3839.com/n/hykb/cornfarm/ajax_daily.php"
        data = {
            "ac": "DailyShareLing",
            "smdeviceid": "BOMLz9iBlx4KwA+wayGk+H/+P91GAH9pC0q9dvBQcvwlVTppakJAfBnJr1K5lyBgzXtIcTgeBqAXtI7NWFaaz8A==",
            "verison": "1.5.7.507",
            "id": "{}".format(task_items["bmh_task_id"]),
            "r": f"0.{random.randint(100000000000000, 8999999999999999)}",
            "scookie": self.cookie,
            "device": "kbA25014349F11473F467DC6FF5C89E9D6"
        }
        response = await self.client.post(url=url, json=data)
        try:
            response_json = response.json()
            if response_json["key"] == "ok" and response_json["message"] == "成功":
                fn_print(
                    f"任务: {task_items['bmh_task_title']}- ✅奖励领取成功！\n成熟度+{response_json['reward_csd_num']}\n已完成任务数量：{response_json['daily_renwu_success_total']}\n今日获得成熟度{response_json['daily_day_all_chengshoudu']}")
            else:
                fn_print("奖励领取失败！")
        except Exception:
            print(response.text)

    async def task(self):
        cookie = urllib.parse.quote(self.cookie) if "|" in self.cookie else self.cookie
        await self.get_task_ids()
        await self.get_bmh_task_ids()

        for item, bmh_item in self.items, self.bmh_tasks:
            if not await self.process_item(item, bmh_item):
                break
        # if self.temp_id:
        #     print("等待体验结束...")
        #     time.sleep(60)
        #     for ty_id in self.temp_id:
        #         await self.get_task("login", ty_id)
        #         data = await self.get_task("signToday", ty_id)
        #         key = str(data["key"])
        #         if key == "-1005":
        #             print("体验游戏中,请一分钟后再刷新领取☑️")
        #             await self.get_task("tiyan", id)
        #             self.temp_id.append(id)  # 将正在体验的活动id加入列表中
        #         elif key == "-1007":
        #             await self.get_task("sharelimit", id)
        #             print(f"活动【{item['title']}】分享成功！✅")
        #             await self.get_task("login", id)
        #             await self.get_task("signToday", id)
        #         elif key == "-1002":
        #             print(f"活动【{item['title']}】奖励已领取过了！")
        #         elif key == "200":
        #             print(f"活动【{item['title']}】签到成功！✅已签到{data['signnum']}天")
        #         elif key == "no_login":
        #             print("⚠️⚠️scookie失效,请重新配置⚠️⚠️")
        await self.client.aclose()


async def run_single_task(cookie):
    ht = AsyncHykbTasks(cookie)
    await ht.task()


async def run_all_tasks(cookies):
    tasks = [run_single_task(cookie) for cookie in cookies]
    await asyncio.gather(*tasks)


async def main():
    hykb_cookie = []
    await run_all_tasks(hykb_cookie)


if __name__ == '__main__':
    asyncio.run(main())
    send_notification_message_collection("好游快爆活动奖励领取通知 - {}".format(datetime.now().strftime("%Y/%m/%d")))
