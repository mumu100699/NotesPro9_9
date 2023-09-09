"""
======================
Author:cc
Time:2023/8/29 17:36
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
from parameterized import parameterized  # 参数化实现


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteSvrSetNoteGetContent']['path']
    host = envConfig['host']
    url = host + path  # # 上传/更新便签信息主体
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def test01_major(self):
        """获取便签内容，主流程校验"""
        info('获取便签内容')
        # 下面的noteid从接口1返回取出来
        body = {
            'noteIds': ['1693318483545_noteId', '1693318483252_noteId']

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'noteBodies': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    @parameterized.expand(('noteIds',))
    def test02_must_key(self, key):
        """获取便签内容，必填项校验"""
        info('获取便签内容')
        print(f'必填项校验的字段{key}')
        print('前置步骤：上传便签信息主体')
        # 下面的noteid从接口1返回取出来
        body = {
            'noteIds': ['1693318483545_noteId', '1693318483252_noteId']

        }
        body.pop(key)  # 必填项校验，去掉这个，会报错

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
