"""
======================
Author:cc
Time:2023/9/8 16:38
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
import datetime
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
    path = apiConfig['ViewCalendarNotes']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase03_input(self):
        """查看日历下便签，入参校验，检验字符串为None,key:remindStartTime"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = None
        # datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase04_input(self):
        """查看日历下便签，入参校验，检验字符串为None,key:remindEndTime"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = None
        # datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase05_input(self):
        """查看日历下便签，入参校验，检验字符串为中文,key:remindEndTime"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = '一二'
        # datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase06_input(self):
        """查看日历下便签，入参校验，检验字符串为中文,key:remindStartTime"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = '一二三四'
        # datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase07_input(self):
        """查看日历下便签，入参校验，检验字符串为特殊字符,key:remindStartTime"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = '@#￥%'
        # datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())