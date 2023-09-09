"""
======================
Author:cc
Time:2023/9/8 17:26
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from common.ymlOperation import ReadYaml
from common.caseLogMethod import info, error, warn, class_case_log
import json
from businessCommon.apiRe import ApiRe
from parameterized import parameterized


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['ViewRecycle']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase02_input(self):
        """查看回收站下便签列表，入参校验，校验参数字符串为空,startIndex"""
        info('查看回收站下便签列表')

        startIndex = ''  # 0
        rows = 10
        aa = self.url.format('', userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)

        res = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(404, res.status_code)
        print(res.json())
        expect_output = {'timestamp': str, 'status': int, 'error': str, 'message': str, 'path': str}
        CheckTools().check_output(expect_output, res.json())
        return res.json()

    def testCase03_input(self):
        """查看回收站下便签列表，入参校验，校验参数字符串为空,rows"""
        info('查看回收站下便签列表')

        startIndex = 0  # 0
        rows = ''  # 10
        aa = self.url.format('', userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)

        res = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(404, res.status_code)
        print(res.json())
        expect_output = {'timestamp': str, 'status': int, 'error': str, 'message': str, 'path': str}
        CheckTools().check_output(expect_output, res.json())
        return res.json()

    def testCase04_input(self):
        """查看回收站下便签列表，入参校验，校验参数字符串为中文,rows"""
        info('查看回收站下便签列表')

        startIndex = 0  # 0
        rows = '一二三四'  # 10
        aa = self.url.format('', userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)

        res = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        return res.json()

    def testCase05_input(self):
        """查看回收站下便签列表，入参校验，校验参数字符串为None,key:rows"""
        info('查看回收站下便签列表')

        startIndex = 0  # 0
        rows = None  # 10
        aa = self.url.format('', userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)

        res = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        return res.json()

    def testCase06_input(self):
        """查看回收站下便签列表，入参校验，校验参数字符串为None,key:startIndex"""
        info('查看回收站下便签列表')

        startIndex = None  # 0
        rows = 10  # 10
        aa = self.url.format('', userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)

        res = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        return res.json()
