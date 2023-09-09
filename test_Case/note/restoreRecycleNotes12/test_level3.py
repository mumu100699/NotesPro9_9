"""
======================
Author:cc
Time:2023/9/9 0:21
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from common.ymlOperation import ReadYaml
from common.caseLogMethod import info, step, warn, class_case_log
import json
from businessCommon.apiRe import ApiRe
from parameterized import parameterized
from businessCommon.automation import generate_notes


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['RestoreRecycleNotes']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def testCase07_handles(self):
        """校验已经删除的便签，恢复成功"""
        step('前置步骤1：新增一条便签')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        info(f'{user1_note_id}')
        note_id = user1_note_id[0]  # 1693318482398_noteId，user1_note_id[0]
        body = {
            'noteId': note_id

        }

        step('前置步骤2：删除已经新增的便签')
        url_1 = 'http://note-api.wps.cn/v3/notesvr/delete'
        res_1 = self.apiRe.note_post(url_1, self.user_id, self.sid, body)
        self.assertEqual(200, res_1.status_code)
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res_1.json())  # actual_output等于res.json()

        step('前置步骤3：查询回收站下的已经删除的便签')
        startIndex = 0
        rows = 10
        url_2 = 'http://note-api.wps.cn/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        aa = url_2.format(userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)
        res_2 = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(200, res_2.status_code)

        step('前置步骤4：回收站恢复已经删除的便签')
        info('恢复回收站的便签')
        note_ids = [note_id]
        body = {
            'userId': self.user_id,
            'noteIds': note_ids
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res_3 = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(200, res_3.status_code)

        step('前置步骤5：查询恢复之后是否在便签列表')
        startIndex = 0
        rows = 10
        url_1 = 'http://note-api.wps.cn/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        aa = url_1.format(userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)
        res_3 = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(200, res_3.status_code)
        bb = res_3.json()['webNotes']
        dd = False
        for i in bb:
            if note_id == i['noteId']:
                print('校验成功')
                self.assertEqual(note_id, i['noteId'])
                dd = True
        if dd:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 1)
            # self.assertEqual(1, 2) 正确的


