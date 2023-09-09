"""
======================
Author:cc
Time:2023/9/6 17:57
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
    apiRe = ApiRe()

    def testCase03_input(self):
        """新增分组：入参校验，检验字符串为空，key:groupId"""
        info('新增分组')

        group_id = ''  # str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase04_input(self):
        """新增分组：入参校验，检验字符串为空，key:group_name"""
        info('新增分组')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = ''  # str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase05_input(self):
        """新增分组：入参校验，检验字符串为中文，key:groupId"""
        info('新增分组')

        group_id = '一二三四'  # str(int(time.time() * 1000)) + '_groupId'
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

    def testCase06_input(self):
        """新增分组：入参校验，检验字符串为None，key:groupId"""
        info('新增分组')

        group_id = None  # str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase07_input(self):
        """新增分组：入参校验，检验字符串为特殊字符，key:groupId"""
        info('新增分组')

        group_id = '@#$'  # str(int(time.time() * 1000)) + '_groupId'
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
