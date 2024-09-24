# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         hykb_tasks.py
# @author           Echo
# @EditTime         2024/9/24
import asyncio
import random
import re
import urllib.parse
from datetime import datetime
import os
import httpx
from bs4 import BeautifulSoup

if 'Hykb_cookie' in os.environ:
    hykb_cookie = re.split("@|&", os.environ.get("Hykb_cookie"))
    print(f"查找到{len(hykb_cookie)}个账号")
else:
    hykb_cookie = []
    print("未查找到Hykb_cookie变量.")
    exit()


class AsyncHykbTasks:
    def __init__(self, cookie):
        self.client = httpx.AsyncClient(base_url="https://huodong3.3839.com", verify=False)
        self.cookie = cookie
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

    async def get_task(self, a, hd_id_):
        try:
            response = await self.client.post(
                url="/n/hykb/signcard/ajax.php",
                content=f"ac={a}&t={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}&r=0.{random.randint(1000000000000000, 8999999999999999)}&hd_id={hd_id_}&hd_id2={hd_id_}&scookie={self.cookie}",
            )
            return response.json()
        except Exception as e:
            print(f"Error in get_task: {e}")
            return None

    async def process_item(self, item):
        id = item["id"]
        await self.get_task("login", id)
        data = await self.get_task("signToday", id)

        key = data["key"]
        if key == "-1005":
            print("体验游戏中,请一分钟后再刷新领取☑️")
            await self.get_task("tiyan", id)
        elif key == "-1007":
            await self.get_task("sharelimit", id)
            print(f"活动【{item['title']}】分享成功！✅")
            await self.get_task("login", id)
            await self.get_task("signToday", id)
        elif key == "-1002":
            print(f"活动【{item['title']}】奖励已领取过了！")
        elif key == "200":
            print(f"活动【{item['title']}】签到成功！✅已签到{data['signnum']}天")
        elif key == "no_login":
            print("⚠️⚠️scookie失效,请重新配置⚠️⚠️")
            return False
        return True

    async def task(self):
        self.cookie = urllib.parse.quote(self.cookie) if "|" in self.cookie else self.cookie
        await self.get_task_ids()

        for item in self.items:
            if not await self.process_item(item):
                break

        await self.client.aclose()


async def run_single_task(cookie):
    ht = AsyncHykbTasks(cookie)
    await ht.task()


async def run_all_tasks(cookies):
    tasks = [run_single_task(cookie) for cookie in cookies]
    await asyncio.gather(*tasks)


async def main():
    ht = AsyncHykbTasks(hykb_cookie)
    await ht.task()


if __name__ == '__main__':
    asyncio.run(main())
