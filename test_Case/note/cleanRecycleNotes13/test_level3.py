"""
======================
Author:cc
Time:2023/9/9 9:15
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
from test_Case.note.viewRecycleNoteList11.test_level1 import TestPro
from parameterized import parameterized
from businessCommon.automation import generate_notes


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['CleanRecycleNotes']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()
    pro = TestPro()

    def testCase07_handles(self):
        """清除回收站便签，校验清空所有已经删除的便签"""
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

        # step('前置步骤3：查询回收站下的已经删除的便签')
        # startIndex = 0
        # rows = 10
        # url_2 = 'http://note-api.wps.cn/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        # aa = url_2.format(userid=self.user_id, startindex=startIndex, rows=rows)
        # print(aa)
        # res_2 = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        # self.assertEqual(200, res_2.status_code)

        info('查看回收站下便签列表')
        step('前置步骤3：查询回收站下的已经删除的便签')
        startIndex = 0
        rows = 999
        url_1 = 'http://note-api.wps.cn/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        aa = url_1.format(userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)
        res_1 = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(200, res_1.status_code)
        cc = []
        for i in res_1.json()['webNotes']:
            cc.append(i['noteId'])

        step('前置步骤4：清空回收站')
        body = {
            'noteIds': cc
        }

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res_2.status_code)
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res_2.json())