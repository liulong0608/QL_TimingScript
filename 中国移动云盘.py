# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         中国移动云盘.py
# @author           Echo
# @EditTime         2024/11/4
# corn: 0 0 8,16,20 * * *
# const $ = new Env('中国移动云盘');
import asyncio
import random
import time

import httpx

ua = "Mozilla/5.0 (Linux; Android 11; M2012K10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.210 Mobile Safari/537.36 MCloudApp/10.0.1"


class MobileCloudDisk:
    def __init__(self, cookie):
        self.client = httpx.AsyncClient(verify=False)
        self.notebook_id = None
        self.note_token = None
        self.note_auth = None
        self.click_num = 15  # 定义抽奖次数和摇一摇戳一戳次数
        self.draw = 1  # 定义抽奖次数，首次免费
        self.timestamp = str(int(round(time.time() * 1000)))
        self.cookies = {'sensors_stay_time': self.timestamp}
        self.Authorization = cookie.split("#")[0]
        self.account = cookie.split("#")[1]
        self.auth_token = cookie.split("#")[2]
        self.JwtHeaders = {
            'User-Agent': ua,
            'Accept': '*/*',
            'Host': 'caiyun.feixin.10086.cn:7071'
        }
        self.treetHeaders = {
            'Host': 'happy.mail.10086.cn',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': ua,
            'Referer': 'https://happy.mail.10086.cn/jsp/cn/garden/wap/index.html?sourceid=1003',
            'Cookie': ''
        }

    async def refresh_token(self):
        responses = await self.client.post(
            url='https://orches.yun.139.com/orchestration/auth-rebuild/token/v1.0/querySpecToken',
            headers={
                'Authorization': self.Authorization,
                'User-Agent': ua,
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': 'orches.yun.139.com'
            },
            json={
                "account": self.account,
                "toSourceId": "001005"
            }
        )
        refresh_token_responses = responses.json()
        if refresh_token_responses["success"]:
            refresh_token = refresh_token_responses["data"]["token"]
            return refresh_token
        else:
            print(refresh_token_responses)
            return None

    async def jwt(self):
        token = await self.refresh_token()
        if token is not None:
            jwt_url = f"https://caiyun.feixin.10086.cn:7071/portal/auth/tyrzLogin.action?ssoToken={token}"
            jwt_response = await self.client.post(
                url=jwt_url,
                headers=self.JwtHeaders
            )
            jwt_datas = jwt_response.json()
            if jwt_datas["code"] != 0:
                print(jwt_datas["msg"])
                return False
            self.JwtHeaders["jwtToken"] = jwt_datas["result"]["token"]
            self.cookies["jwtToken"] = jwt_datas["result"]["token"]
            return True
        else:
            print("cookie可能失效了")
            return False

    async def query_sign_in_status(self):
        """
        查询签到状态
        :return: 
        """
        sign_response_datas = await self.client.get(
            url="https://caiyun.feixin.10086.cn/market/signin/page/info?client=app",
            headers=self.JwtHeaders,
            cookies=self.cookies
        )
        if sign_response_datas.status_code == 200:
            sign_response_data = sign_response_datas.json()
            if sign_response_data["msg"] == "success":
                today_sign = sign_response_data["result"].get("todaySignIn", False)
                if today_sign:
                    print(f"用户【{self.account}】，===今日已签到☑️===")
                else:
                    await self.sign_in()
        else:
            print(f"签到查询状态异常：{sign_response_datas.status_code}")

    async def a_poke(self):
        """
        戳一戳
        :return: 
        """
        url = "https://caiyun.feixin.10086.cn/market/signin/task/click?key=task&id=319"
        successful_click = 0  # 获得次数
        try:
            for _ in range(self.click_num):
                responses = await self.client.get(
                    url=url,
                    headers=self.JwtHeaders,
                    cookies=self.cookies
                )
                time.sleep(0.5)
                if responses.status_code == 200:
                    responses_data = responses.json()
                    if "result" in responses_data:
                        print(f"用户【{self.account}】，===戳一戳成功✅✅===, {responses_data['result']}")
                        successful_click += 1
                else:
                    print(f"戳一戳发生异常：{responses.status_code}")
            if successful_click == 0:
                print(f"用户【{self.account}】，===未获得 x {self.click_num}===")
        except Exception as e:
            print(f"戳一戳执行异常：{e}")

    async def refresh_notetoken(self):
        """
        刷新noteToken
        :return: 
        """
        note_url = 'http://mnote.caiyun.feixin.10086.cn/noteServer/api/authTokenRefresh.do'
        note_payload = {
            "authToken": self.auth_token,
            "userPhone": self.account
        }
        note_headers = {
            'X-Tingyun-Id': 'p35OnrDoP8k;c=2;r=1122634489;u=43ee994e8c3a6057970124db00b2442c::8B3D3F05462B6E4C',
            'Charset': 'UTF-8',
            'Connection': 'Keep-Alive',
            'User-Agent': 'mobile',
            'APP_CP': 'android',
            'CP_VERSION': '3.2.0',
            'x-huawei-channelsrc': '10001400',
            'Host': 'mnote.caiyun.feixin.10086.cn',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept-Encoding': 'gzip'
        }
        try:
            response = await self.client.post(
                url=note_url,
                data=note_payload,
                headers=note_headers
            )
            if response.status_code == 200:
                response.raise_for_status()
        except Exception as e:
            print('出错了:', e)
            return
        self.note_token = response.headers.get('NOTE_TOKEN')
        self.note_auth = response.headers.get('APP_AUTH')

    async def get_task_list(self, url, app_type):
        """
        获取任务列表
        :return: 
        """
        task_url = f'https://caiyun.feixin.10086.cn/market/signin/task/taskList?marketname={url}'
        task_response = await self.client.get(
            url=task_url,
            headers=self.JwtHeaders,
            cookies=self.cookies
        )
        if task_response.status_code == 200:
            task_list = {}
            task_response_data = task_response.json()
            await self.rm_sleep()
            if task_response_data["msg"] == "success":
                task_list = task_response_data.get("result", {})
            try:
                for task_type, tasks in task_list.items():
                    if task_type in ["new", "hidden", "hiddenabc"]:
                        continue
                    if app_type == "cloud_app":
                        if task_type == "month":
                            print("\n🗓️云盘每月任务")
                            for month in tasks:
                                task_id = month.get("id")
                                if task_id in [110, 113, 417, 409]:
                                    continue
                                task_name = month.get("name", "")
                                task_status = month.get("state", "")

                                if task_status == "FINISH":
                                    print(f"【{self.account}】，===任务【{task_name}】已完成✅✅===")
                                    continue
                                print(f"【{self.account}】，===任务【{task_name}】待完成✒️✒️===")
                                await self.do_task(task_id, task_type="month", app_type="cloud_app")
                                await asyncio.sleep(2)
                        elif task_type == "day":
                            print("\n🗓️云盘每日任务")
                            for day in tasks:
                                task_id = day.get("id")
                                if task_id == 404:
                                    continue
                                task_name = day.get("name", "")
                                task_status = day.get("state", "")
                                if task_status == "FINISH":
                                    print(f"【{self.account}】，===任务【{task_name}】已完成✅✅===")
                                    continue
                                print(f"【{self.account}】，===任务【{task_name}】待完成✒️✒️===")
                                await self.do_task(task_id, task_type="day", app_type="cloud_app")
                    elif app_type == "email_app":
                        if task_type == "month":
                            print("\n🗓️139邮箱每月任务")
                            for month in tasks:
                                task_id = month.get("id")
                                task_name = month.get("name", "")
                                task_status = month.get("state", "")
                                if task_id in [1004, 1005, 1015, 1020]:
                                    continue
                                if task_status == "FINISH":
                                    print(f"【{self.account}】，===任务【{task_name}】已完成✅✅===")
                                    continue
                                print(f"【{self.account}】，===任务【{task_name}】待完成✒️✒️===")
                                await self.do_task(task_id, task_type="month", app_type="email_app")
                                await asyncio.sleep(2)
            except Exception as e:
                print(f"任务列表获取异常，错误信息：{e}")

    async def do_task(self, task_id, task_type, app_type):
        """
        执行任务
        :param task_id: 
        :param task_type: 
        :param app_type: 
        :return: 
        """
        await self.rm_sleep()
        task_url = f'https://caiyun.feixin.10086.cn/market/signin/task/click?key=task&id={task_id}'
        task_response = await self.client.get(
            url=task_url,
            headers=self.JwtHeaders,
            cookies=self.cookies
        )
        if app_type == "cloud_app":
            if task_type == "day":
                if task_id == 106:
                    await self.upload_file()
                elif task_id == 107:
                    await self.refresh_notetoken()
                    await self.get_notebook_id()
            elif task_type == "month":
                pass
        elif app_type == "email_app":
            if task_type == "month":
                pass

    async def sign_in(self):
        """
        签到
        :return: 
        """
        sign_in_url = 'https://caiyun.feixin.10086.cn/market/manager/commonMarketconfig/getByMarketRuleName?marketName=sign_in_3'
        sign_in_response = await self.client.get(
            url=sign_in_url,
            headers=self.JwtHeaders,
            cookies=self.cookies
        )
        if sign_in_response.status_code == 200:
            sign_in_response_data = sign_in_response.json()
            if sign_in_response_data["msg"] == "success":
                print(f"用户【{self.account}】，===签到成功✅✅===")
            else:
                print(sign_in_response_data)
        else:
            print(f"签到发生异常：{sign_in_response.status_code}")

    async def get_notebook_id(self):
        """
        获取笔记的默认id
        :return: 
        """
        note_url = 'http://mnote.caiyun.feixin.10086.cn/noteServer/api/syncNotebookV3.do'
        headers = {
            'X-Tingyun-Id': 'p35OnrDoP8k;c=2;r=1122634489;u=43ee994e8c3a6057970124db00b2442c::8B3D3F05462B6E4C',
            'Charset': 'UTF-8',
            'Connection': 'Keep-Alive',
            'User-Agent': 'mobile',
            'APP_CP': 'android',
            'CP_VERSION': '3.2.0',
            'x-huawei-channelsrc': '10001400',
            'APP_NUMBER': self.account,
            'APP_AUTH': self.note_auth,
            'NOTE_TOKEN': self.note_token,
            'Host': 'mnote.caiyun.feixin.10086.cn',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': '*/*'
        }
        payload = {
            "addNotebooks": [],
            "delNotebooks": [],
            "notebookRefs": [],
            "updateNotebooks": []
        }
        note_response = await self.client.post(
            url=note_url,
            headers=headers,
            json=payload
        )
        if note_response.status_code == 200:
            note_response_data = note_response.json()
            self.notebook_id = note_response_data["notebooks"][0]["notebookId"]
            if self.notebook_id:
                await self.create_note(headers)
        else:
            print(f"获取笔记id发生异常：{note_response.status_code}")

    async def create_note(self, headers):
        """
        创建笔记
        :return: 
        """
        note_id = await self.random_genner_note_id(length=32)
        create_time = str(int(round(time.time() * 1000)))
        await asyncio.sleep(3)
        update_time = str(int(round(time.time() * 1000)))
        create_note_url = 'http://mnote.caiyun.feixin.10086.cn/noteServer/api/createNote.do'
        payload = {
            "archived": 0,
            "attachmentdir": note_id,
            "attachmentdirid": "",
            "attachments": [],
            "audioInfo": {
                "audioDuration": 0,
                "audioSize": 0,
                "audioStatus": 0
            },
            "contentid": "",
            "contents": [{
                "contentid": 0,
                "data": "<font size=\"3\">000000</font>",
                "noteId": note_id,
                "sortOrder": 0,
                "type": "RICHTEXT"
            }],
            "cp": "",
            "createtime": create_time,
            "description": "android",
            "expands": {
                "noteType": 0
            },
            "latlng": "",
            "location": "",
            "noteid": note_id,
            "notestatus": 0,
            "remindtime": "",
            "remindtype": 1,
            "revision": "1",
            "sharecount": "0",
            "sharestatus": "0",
            "system": "mobile",
            "tags": [{
                "id": self.notebook_id,
                "orderIndex": "0",
                "text": "默认笔记本"
            }],
            "title": "00000",
            "topmost": "0",
            "updatetime": update_time,
            "userphone": self.account,
            "version": "1.00",
            "visitTime": ""
        }
        create_note_response = await self.client.post(
            url=create_note_url,
            headers=headers,
            json=payload
        )
        if create_note_response.status_code == 200:
            print(f"用户【{self.account}】，===创建笔记成功✅✅===")
        else:
            print(f"创建笔记发生异常：{create_note_response.status_code}")

    async def upload_file(self):
        """
        上传文件
        :return: 
        """
        url = 'http://ose.caiyun.feixin.10086.cn/richlifeApp/devapp/IUploadAndDownload'
        headers = {
            'x-huawei-uploadSrc': '1', 'x-ClientOprType': '11', 'Connection': 'keep-alive', 'x-NetType': '6',
            'x-DeviceInfo': '6|127.0.0.1|1|10.0.1|Xiaomi|M2012K10C|CB63218727431865A48E691BFFDB49A1|02-00-00-00-00-00|android 11|1080X2272|zh||||032|',
            'x-huawei-channelSrc': '10000023', 'x-MM-Source': '032', 'x-SvcType': '1', 'APP_NUMBER': self.account,
            'Authorization': self.Authorization,
            'X-Tingyun-Id': 'p35OnrDoP8k;c=2;r=1955442920;u=43ee994e8c3a6057970124db00b2442c::8B3D3F05462B6E4C',
            'Host': 'ose.caiyun.feixin.10086.cn', 'User-Agent': 'okhttp/3.11.0',
            'Content-Type': 'application/xml; charset=UTF-8', 'Accept': '*/*'
        }
        payload = '''                                <pcUploadFileRequest>                                    <ownerMSISDN>{phone}</ownerMSISDN>                                    <fileCount>1</fileCount>                                    <totalSize>1</totalSize>                                    <uploadContentList length="1">                                        <uploadContentInfo>                                            <comlexFlag>0</comlexFlag>                                            <contentDesc><![CDATA[]]></contentDesc>                                            <contentName><![CDATA[000000.txt]]></contentName>                                            <contentSize>1</contentSize>                                            <contentTAGList></contentTAGList>                                            <digest>C4CA4238A0B923820DCC509A6F75849B</digest>                                            <exif/>                                            <fileEtag>0</fileEtag>                                            <fileVersion>0</fileVersion>                                            <updateContentID></updateContentID>                                        </uploadContentInfo>                                    </uploadContentList>                                    <newCatalogName></newCatalogName>                                    <parentCatalogID></parentCatalogID>                                    <operation>0</operation>                                    <path></path>                                    <manualRename>2</manualRename>                                    <autoCreatePath length="0"/>                                    <tagID></tagID>                                    <tagType></tagType>                                </pcUploadFileRequest>                            '''.format(
            phone=self.account)
        response = await self.client.post(
            url=url,
            headers=headers,
            content=payload
        )
        if response is None:
            return
        if response.status_code != 200:
            print(f"上传文件发生异常：{response.status_code}")
        print(f"用户【{self.account}】，===上传文件成功✅✅===")

    async def rm_sleep(self, min_delay=1, max_delay=1.5):
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)

    async def random_genner_note_id(self, length):
        characters = '19f3a063d67e4694ca63a4227ec9a94a19088404f9a28084e3e486b928039a299bf756ebc77aa4f6bfa250308ec6a8be8b63b5271a00350d136d117b8a72f39c5bd15cdfd350cba4271dc797f15412d9f269e666aea5039f5049d00739b320bb9e8585a008b52c1cbd86970cae9476446f3e41871de8d9f6112db94b05e5dc7ea0a942a9daf145ac8e487d3d5cba7cea145680efc64794d43dd15c5062b81e1cda7bf278b9bc4e1b8955846e6bc4b6a61c28f831f81b2270289e5a8a677c3141ddc9868129060c0c3b5ef507fbd46c004f6de346332ef7f05c0094215eae1217ee7c13c8dca6d174cfb49c716dd42903bb4b02d823b5f1ff93c3f88768251b56cc'
        note_id = ''.join(random.choice(characters) for _ in range(length))
        return note_id

    async def run(self):
        if await self.jwt():
            print("=========开始签到=========")
            await self.query_sign_in_status()
            print("=========开始执行戳一戳=========")
            await self.a_poke()
            await self.get_task_list(url="sign_in_3", app_type="cloud_app")
            print("=========开始执行☁️云朵大作战=========")
            # todo
            


async def main():
    ck = "Basic bW9iaWxlOjE4NTgyODUyMjYzOkdPVHpqTnRtfDF8UkNTfDE3MzMyOTcwODYzMzZ8UGdPVkZ6V1JWYjdSRjJ1Y3pNejNJd1o5b3FiYzJzNmw5QVdWMTlNZk1HdEt4LndXa2t4SkE2cmZEcGZWaUNBU1UyVW94dW9zSXNnZUxUVk9IWnczajd5Q1AzNnM3SEk5MDhFMDRRVm1FVjcwTWJjQXNDU3pLcEV0UlRpQ1pkUVFnUUdZcXpCVW5IeDhQak55QW1UbTRFb2pvQkRxMVBqVHdCcXBuZnNCTDFvLQ==#18582852263#STuid0000011730705776084kKnQ1rbi1wnexE5CovnoFuxLUtnkrgLL"
    mobileCloudDisk = MobileCloudDisk(ck)
    await mobileCloudDisk.run()


if __name__ == '__main__':
    asyncio.run(main())
