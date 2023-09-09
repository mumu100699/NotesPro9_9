"""
======================
Author:cc
Time:2023/8/31 22:52
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

    def testCase01_major(self):
        """查看日历下便签，主流程校验"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        # remind_start_time = int(time.time() * 1000)
        # remind_end_time = int(time.time() * 1000)

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'responseTime': int, 'webNotes': list}
        CheckTools().check_output(expect_output, res.json())

    @parameterized.expand(('remindStartTime', 'remindEndTime'))  # 'startIndex', 'rows'
    def testCase02_must_key(self, key):
        """查看日历下便签，必填项校验，remindStartTime，remindEndTime"""
        info('查看日历下便签')
        print(f'必填项校验的字段{key}')

        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }
        body.pop(key)

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())