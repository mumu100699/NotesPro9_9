import unittest
import requests
import time
from common.checkCommon import CheckTools
from common.ymlOperation import ReadYaml
from common.caseLogMethod import info, error, warn, class_case_log
import json
from businessCommon.apiRe import ApiRe
from parameterized import parameterized

"""
======================
Author:cc
Time:2023/8/26 22:33
Project: python0731
love:xz
=======================
"""


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()  # 读取yml文件的方法，实例化，设置一个变量envConfig接收
    print(envConfig)
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteSvrSetNoteInfo']['path']
    host = envConfig['host']
    url = host + path  # # 上传/更新便签信息主体
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    # @unittest.skip('未完成')  # 暂时取消执行用例
    def test01_major(self):  # 必须test开头命名
        """上传/更新便签主体主流程"""
        # info(self._testMethodName)
        # info(self._testMethodDoc)
        info('上传/更新便签主体')

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    @parameterized.expand(('noteId', ))
    def test02_must_key(self, key):  # 必须test开头命名
        """上传/更新便签主体主流程，必填项校验noteId"""
        info('上传/更新便签主体')
        print(f'必填项校验的字段{key}')

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }
        body.pop(key)

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()




