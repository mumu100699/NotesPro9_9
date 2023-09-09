"""
======================
Author:cc
Time:2023/9/8 18:14
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

    def testCase03_input(self):
        """清除回收站便签，入参校验，校验参数字符串为空key:noteIds"""
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
            'noteIds': ''  # cc
        }

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res_2.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res_2.json())

    def testCase04_input(self):
        """清除回收站便签，入参校验，校验参数字符串为中文key:noteIds"""
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
            'noteIds': '一二三四'  # cc
        }

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res_2.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res_2.json())

    def testCase05_input(self):
        """清除回收站便签，入参校验，校验参数字符串为特殊字符key:noteIds"""
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
            'noteIds': '@@@@@@@@@@@@@@@@@%'  # cc
        }

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res_2.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res_2.json())

    def testCase06_input(self):
        """清除回收站便签，入参校验，校验参数字符串为None,key:noteIds"""
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
            'noteIds': None  # cc
        }

        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res_2.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res_2.json())