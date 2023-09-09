"""
======================
Author:cc
Time:2023/9/8 17:10
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
from common.caseLogMethod import info, step, warn, class_case_log
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
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def testCase08_handles(self):
        """查看日历下便签，越权查看，用户1查看用户2的日历便签"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid2, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase09_handles(self):
        """查看日历下便签，越权查看，用户2查看用户1的日历便签"""
        info('查看日历下便签')

        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 1, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 9, 1).timestamp()

        body = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }

        res = self.apiRe.note_post(self.url, self.user_id2, self.sid, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase10_handles(self):
        """校验新增日历下的便签，查看是否新增成功"""
        step("前置条件1：新增日历下的便签")
        note_id = str(int(time.time() * 1000)) + '_noteId'
        remindTime = datetime.datetime(2023, 9, 8).timestamp()
        body_1 = {
            'noteId': note_id,
            'remindTime': remindTime
        }
        url_1 = 'http://note-api.wps.cn/v3/notesvr/set/noteinfo'
        res_1 = self.apiRe.note_post(url_1, self.user_id, self.sid, body_1)
        self.assertEqual(200, res_1.status_code)

        step("查看日历下的便签，是否存在")
        current_year = datetime.datetime.now().year
        month_start_timestamp = datetime.datetime(current_year, 8, 1).timestamp()
        month_end_timestamp = datetime.datetime(current_year, 10, 1).timestamp()

        body_2 = {
            'remindStartTime': month_start_timestamp,
            'remindEndTime': month_end_timestamp,
            'startIndex': 0,
            'rows': 50
        }
        res_2 = self.apiRe.note_post(self.url, self.user_id, self.sid, body_2)
        self.assertEqual(200, res_2.status_code)
        webNotes = res_2.json()['webNotes']
        # 查询返回空数组，理论上要生成一个
        self.assertEqual(0, len(webNotes))

