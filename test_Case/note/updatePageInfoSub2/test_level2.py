"""
======================
Author:cc
Time:2023/9/7 16:42
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
from parameterized import parameterized


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
    def test03_input(self):  # 必须test开头命名
        """上传/更新便签主体，入参校验，检验字符串为空，key:noteId"""
        info('上传/更新便签主体')

        note_id = ''  # str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def test04_input(self):  # 必须test开头命名
        """上传/更新便签主体，入参校验，检验字符串为特殊字符，key:noteId"""
        info('上传/更新便签主体')

        note_id = '#@￥%'  # str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def test05_input(self):  # 必须test开头命名
        """上传/更新便签主体，入参校验，检验字符串为null，key:noteId"""
        info('上传/更新便签主体')

        note_id = 'null'  # str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()
