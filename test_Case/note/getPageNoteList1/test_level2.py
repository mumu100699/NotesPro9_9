"""
======================
Author:cc
Time:2023/9/5 23:17
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
    # path = apiConfig['NoteGroup']['path']
    # host = envConfig['host']
    # url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase02_input_empty_str(self):  # 导入空字符串
        """入参校验，校验参数字符串为空，key:start_index"""
        info('获取首页便签数据')
        start_index = ''  # 验证为空，正确的是start_index = 0
        userid = 1145973490
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(404, res.status_code)  # 状态断言
        expect_output = {'timestamp': str, 'status': int, 'error': str, 'message': str, 'path': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        # print(res.status_code)
        # print(res.json())

    def testCase03_input_empty_str(self):  # 导入空字符串
        """入参校验，校验参数字符串为空，key:userid"""
        info('获取首页便签数据')
        start_index = 0
        userid = ''  # 验证为空，正确的是userid = 1145973490
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(404, res.status_code)  # 状态断言
        expect_output = {'timestamp': str, 'status': int, 'error': str, 'message': str, 'path': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def testCase04_input_empty_str(self):  # 导入空字符串
        """入参校验，校验参数字符串为空，key:rows"""
        info('获取首页便签数据')
        start_index = 0
        userid = 1145973490
        rows = ''  # 验证为空，正确的是rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(404, res.status_code)  # 状态断言
        expect_output = {'timestamp': str, 'status': int, 'error': str, 'message': str, 'path': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()



