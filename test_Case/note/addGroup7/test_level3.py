"""
======================
Author:cc
Time:2023/9/8 14:22
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from common.ymlOperation import ReadYaml
from common.caseLogMethod import info, error, warn, class_case_log, step
import json
from businessCommon.apiRe import ApiRe
from parameterized import parameterized


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['AddGroup']['path']
    must_key = apiConfig['AddGroup']['must_key']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def testCase08_handles(self):
        """新增分组，校验用户1使用户2的sid"""
        info('新增分组')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid2, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase09_handles(self):
        """新增分组，校验用户2使用用户1的user_id2"""
        info('新增分组')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }

        res = self.apiRe.note_post(self.url, self.user_id2, self.sid, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase010_handles(self):
        """新增分组，校验新增分组成功"""
        info('新增分组')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'responseTime': int, 'updateTime': int}
        CheckTools().check_output(expect_output, res.json())

        exclude_invalid = ''
        body = {
            'excludeInvalid': exclude_invalid

        }
        url_1 = 'http://note-api.wps.cn/v3/notesvr/get/notegroup'
        res_1 = self.apiRe.note_post(url_1, self.user_id, self.sid, body)
        self.assertEqual(200, res_1.status_code)
        aa = res_1.json()['noteGroups']
        cc = False
        for i in aa:
            if group_id == i['groupId']:
                cc = True
        if cc:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2)