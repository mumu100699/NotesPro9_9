"""
======================
Author:cc
Time:2023/8/31 17:30
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
from parameterized import parameterized  # 参数化实现
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


@class_case_log
class GetGroupList1(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteGroup']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def test01_major(self):
        """获取便签分组列表，主流程校验"""
        info('分组列表')
        exclude_invalid = ''
        body = {
            'excludeInvalid': exclude_invalid

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'requestTime': int, 'noteGroups': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    @parameterized.expand(('excludeInvalid',))
    def test02_must_key(self, key):
        """获取便签分组列表，校验必填项无"""
        info('分组列表')
        print(f'必填项校验的字段{key}')
        exclude_invalid = ''
        body = {
            'excludeInvalid': exclude_invalid

        }
        body.pop(key)

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'requestTime': int, 'noteGroups': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
