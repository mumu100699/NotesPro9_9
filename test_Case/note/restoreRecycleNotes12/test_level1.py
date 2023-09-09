"""
======================
Author:cc
Time:2023/9/1 13:02
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
    path = apiConfig['RestoreRecycleNotes']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase01_major(self):
        """恢复回收站的便签，主流程校验"""
        info('恢复回收站的便签')
        body = {
            'userId': self.user_id,
            'noteIds': ['1693318482398_noteId']
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        # print(res.json())
        # expect_output = {'responseTime': int, 'webNotes': list}
        # CheckTools().check_output(expect_output, res.json())
        # 没有返回参数，所以不执行这个校验

    @parameterized.expand(('userId', ))
    def testCase02_must_key(self, key):
        """恢复回收站的便签，必填项校验key:userId"""
        info('恢复回收站的便签')
        print(f'必填项校验的字段{key}')
        body = {
            'userId': self.user_id,
            'noteIds': ['1693318482398_noteId']
        }
        body.pop(key)
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(412, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    @parameterized.expand(('noteIds', ))
    def testCase03_must_key(self, key):
        """恢复回收站的便签，必填项校验key:noteIds"""
        info('恢复回收站的便签')
        print(f'必填项校验的字段{key}')
        body = {
            'userId': self.user_id,
            'noteIds': ['1693318482398_noteId']
        }
        body.pop(key)
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())