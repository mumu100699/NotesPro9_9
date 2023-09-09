"""
======================
Author:cc
Time:2023/9/8 10:26
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


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteSvrSetNoteGetContent']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def test03_input(self):
        """获取便签内容，入参校验：检验字符串为空，key:noteIds"""
        info('获取便签内容')
        # 下面的noteid从接口1返回取出来
        body = {
            'noteIds': []  # '1693318483545_noteId', '1693318483252_noteId'

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def test04_input(self):
        """获取便签内容，入参校验：检验字符串为特殊字符，key:noteIds"""
        info('获取便签内容')
        # 下面的noteid从接口1返回取出来
        body = {
            'noteIds': ['@#%']  # '1693318483545_noteId', '1693318483252_noteId'

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)  # 特殊字符校验通过，接口有误
        expect_output = {'responseTime': int, 'noteBodies': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def test05_input(self):
        """获取便签内容，入参校验：检验字符串为null，key:noteIds"""
        info('获取便签内容')
        # 下面的noteid从接口1返回取出来
        body = {
            'noteIds': ['null']  # '1693318483545_noteId', '1693318483252_noteId'

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)  # null校验通过，接口有误
        expect_output = {'responseTime': int, 'noteBodies': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
