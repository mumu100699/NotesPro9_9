"""
======================
Author:cc
Time:2023/9/8 17:56
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

    def testCase04_input(self):
        """恢复回收站的便签，入参校验，校验参数字符串为空"""
        info('恢复回收站的便签')
        body = {
            'userId': '',  # self.user_id
            'noteIds': ['1693318482398_noteId']
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(412, res.status_code)
        # print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        # 没有返回参数，所以不执行这个校验

    def testCase05_input(self):
        """恢复回收站的便签，入参校验，校验参数字符串为中文"""
        info('恢复回收站的便签')
        body = {
            'userId': '一二三四',  # self.user_id
            'noteIds': ['1693318482398_noteId']
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        # print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        # 没有返回参数，所以不执行这个校验

    def testCase06_input(self):
        """恢复回收站的便签，入参校验，校验参数字符串为特殊字符"""
        info('恢复回收站的便签')
        body = {
            'userId': '@#￥%',  # self.user_id
            'noteIds': ['1693318482398_noteId']
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        # print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        # 没有返回参数，所以不执行这个校验

    def testCase07_input(self):
        """恢复回收站的便签，入参校验，校验参数字符串为None"""
        info('恢复回收站的便签')
        body = {
            'userId': None,  # self.user_id
            'noteIds': ['1693318482398_noteId']
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(412, res.status_code)
        # print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        # 没有返回参数，所以不执行这个校验

    def testCase08_input(self):
        """恢复回收站的便签，入参校验，校验参数字符串为空,key:noteIds"""
        info('恢复回收站的便签')
        body = {
            'userId': self.user_id,
            'noteIds': []  # ['1693318482398_noteId']
        }
        aa = self.url.format(userid=self.user_id)
        print(aa)
        res = self.apiRe.note_patch(aa, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        # print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())
        # 没有返回参数，所以不执行这个校验