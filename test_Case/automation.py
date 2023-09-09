# 7.批量生成便签的函数  形参定义 num、sid、user_id   return noteids
"""
======================
Author:cc
Time:2023/8/29 22:29
Project: interface828
love:xz
=======================
"""


import requests
import time
from common.checkCommon import CheckTools


def generate_notes(num, sid, user_id):
    note_ids = []
    if num <= 0:
        return
    i = 0
    while i < num:
        # 在这里编写需要重复执行的代码
        # 上传/更新便签主体
        url = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'  # 上传/更新便签信息主体
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': user_id,
            'cookie': 'wps_sid=' + sid
        }

        note_id = str(int(time.time() * 1000)) + '_noteId' + str(i)
        note_ids.append(note_id)  # 把note_id加入列表
        body = {
            'noteId': note_id
        }

        res = requests.post(url=url, headers=headers, json=body)
        print(res.json())
        infoVersion = res.json()['infoVersion']
        print(res.status_code)
        assert(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        # 上传/更新便签内容
        get_userid_url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notecontent'
        title = str(int(time.time() * 1000)) + '_title'
        summary = str(int(time.time() * 1000)) + '_summary'
        body = str(int(time.time() * 1000)) + '_body'

        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': body,
            'localContentVersion': infoVersion,
            'BodyType': 0
        }

        get_userid_res = requests.post(url=get_userid_url, headers=headers, json=body)
        print(get_userid_res.status_code)
        print(get_userid_res.json())
        assert(200, get_userid_res.status_code)
        expect_output = {'responseTime': int, 'contentVersion': 1, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()

        i += 1

    return note_ids


aa = generate_notes(2, 'V02SHITw2Sa6ftb0AJy1dOOrePI8B0g00a9cb574004d65b716', '1298511638')
print(aa)
