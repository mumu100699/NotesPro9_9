"""
======================
Author:cc
Time:2023/9/8 15:45
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
    path = apiConfig['ViewGroup']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase03_input(self):
        """查看分组下的便签，入参校验，检验字符串为空"""
        info('查看分组下的便签')

        group_id = ''  # str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase04_input(self):
        """查看分组下的便签，入参校验，检验字符串为None"""
        info('查看分组下的便签')

        group_id = None  # str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase05_input(self):
        """查看分组下的便签，入参校验，检验字符串为中文"""
        info('查看分组下的便签')

        group_id = '一二三四'  # str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase06_input(self):
        """查看分组下的便签，入参校验，检验字符串为特殊字符"""
        info('查看分组下的便签')

        group_id = '@#￥%'  # str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())