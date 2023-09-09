"""
======================
Author:cc
Time:2023/8/31 22:45
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
    path = apiConfig['DeleteNoteGroup']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase01_major(self):
        """删除分组，主流程校验"""
        info('删除分组')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res.json())

    @parameterized.expand(('groupId',))
    def testCase02_must_key(self, key):
        """删除分组，必填项校验，groupId"""
        info('删除分组')
        print(f'必填项校验的字段{key}')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }
        body.pop(key)

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())