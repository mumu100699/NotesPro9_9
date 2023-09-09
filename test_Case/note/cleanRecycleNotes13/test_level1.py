"""
======================
Author:cc
Time:2023/9/1 13:23
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

    def testCase01_major(self):
        """清除回收站便签，主流程校验"""
        info('查看回收站下便签列表')
        step('前置步骤1：查询回收站列表')
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

        step('前置步骤2：清空回收站')
        body = {
            'noteIds': cc
        }

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res_2.status_code)
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res_2.json())

    @parameterized.expand(('noteIds',))
    def testCase02_must_key(self, key):
        """清除回收站便签，必填项校验key:noteIds"""
        print(f'必填项校验的字段{key}')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        # 下面的noteid从接口1返回取出来
        note_id = user1_note_id[0]  # 1693318482398_noteId
        body = {
            'noteId': note_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        info('查看回收站下便签列表')
        step('前置步骤1：查询回收站列表')
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

        step('前置步骤2：清空回收站')

        body = {
            'noteIds': cc
        }
        body.pop(key)

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res_2.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res_2.json())