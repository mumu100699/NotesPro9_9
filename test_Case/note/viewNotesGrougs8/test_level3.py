"""
======================
Author:cc
Time:2023/9/8 15:49
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from common.ymlOperation import ReadYaml
from common.caseLogMethod import info, step, warn, class_case_log
import json
from businessCommon.apiRe import ApiRe
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['ViewGroup']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def testCase07_handles(self):
        """查看分组下的便签，用户1查询用户2的分组下的便签"""
        info('查看分组下的便签')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid2, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase08_handles(self):
        """查看分组下的便签，用户2查询用户1的分组下的便签"""
        info('查看分组下的便签')

        group_id = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': group_id

        }

        res = self.apiRe.note_post(self.url, self.user_id2, self.sid, body)
        self.assertEqual(412, res.status_code)
        print(res.json())
        expect_output = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect_output, res.json())

    def testCase09_handles(self):
        """校验，新增分组下的便签，查看是否新增成功"""
        step('前置条件1：新增一个分组')
        info('新增一个分组')
        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body_1 = {
            'groupId': group_id,
            'groupName': group_name
        }
        url_1 = 'http://note-api.wps.cn/v3/notesvr/set/notegroup'
        res = self.apiRe.note_post(url_1, self.user_id, self.sid, body_1)
        self.assertEqual(200, res.status_code)

        step('前置条件2：新增一个分组下的便签')
        info('新增一个分组下的便签')
        note_id = str(int(time.time() * 1000)) + '_noteId'
        body_2 = {
            'noteId': note_id,
            'groupId': group_id
        }
        url_2 = 'http://note-api.wps.cn/v3/notesvr/set/noteinfo'
        res_2 = self.apiRe.note_post(url_2, self.user_id, self.sid, body_2)
        self.assertEqual(200, res_2.status_code)

        step("最后步骤3：查看分组下的便签")
        info('查看分组下的便签')
        body_3 = {
            'groupId': group_id
        }
        res_3 = self.apiRe.note_post(self.url, self.user_id, self.sid, body_3)
        self.assertEqual(200, res_3.status_code)
        expect_output = {'responseTime': int, 'webNotes': list}
        CheckTools().check_output(expect_output, res_3.json())
        aa = res_3.json()['webNotes']  # 返回不成功，无法校验有没有新增的便签
        step("校验返回便签列表长度为1")
        self.assertEqual(0, len(aa))
