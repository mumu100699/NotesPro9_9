"""
======================
Author:cc
Time:2023/8/31 17:11
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
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteDelete']['path']
    host = envConfig['host']
    url = host + path  # # 上传/更新便签信息主体
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def test01_major(self):
        """删除便签，校验主流程"""
        info('删除便签')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        # 下面的noteid从接口1返回取出来
        note_id = user1_note_id[0]  # 1693318482398_noteId
        body = {
            'noteId': note_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    @parameterized.expand(('noteId',))
    def test02_must_key(self, key):
        """删除便签，必填项note_id"""
        info('删除便签')
        print(f'必填项校验的字段{key}')
        # 下面的noteid从接口1返回取出来
        note_id = '1693318482398_noteId'
        body = {
            'noteId': note_id

        }
        body.pop(key)

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
