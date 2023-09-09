"""
======================
Author:cc
Time:2023/9/8 13:58
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
from parameterized import parameterized  # 参数化实现
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteGroup']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def test06_handles(self):
        """校验用户1新增一个分组，用户1查询分组是否存在已新增的"""
        info('新增一个分组')
        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }
        url_1 = 'http://note-api.wps.cn/v3/notesvr/set/notegroup'
        res_1 = self.apiRe.note_post(url_1, self.user_id, self.sid, body)
        self.assertEqual(200, res_1.status_code)

        info('查询分组列表')
        exclude_invalid = ''
        body = {
            'excludeInvalid': exclude_invalid

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        aa = res.json()['noteGroups']
        expect_output = {'requestTime': int, 'noteGroups': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
        cc = False
        for i in aa:
            if group_id == i['groupId']:
                cc = True
        if cc:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2)

    def test07_handles(self):
        """越权校验，用户1新增分组，用户2查询分组列表"""
        info('新增一个分组')
        group_id = str(int(time.time() * 1000)) + '_groupId'
        group_name = str(int(time.time() * 1000)) + '_groupName'
        body = {
            'groupId': group_id,
            'groupName': group_name
        }
        url_1 = 'http://note-api.wps.cn/v3/notesvr/set/notegroup'
        res_1 = self.apiRe.note_post(url_1, self.user_id, self.sid, body)
        self.assertEqual(200, res_1.status_code)

        info('查询分组列表')
        exclude_invalid = ''
        body = {
            'excludeInvalid': exclude_invalid

        }

        res = self.apiRe.note_post(self.url, self.user_id2, self.sid2, body)
        self.assertEqual(200, res.status_code)
        aa = res.json()['noteGroups']
        expect_output = {'requestTime': int, 'noteGroups': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
        cc = True
        for i in aa:
            if group_id == i['groupId']:
                cc = False
        if cc:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2)
