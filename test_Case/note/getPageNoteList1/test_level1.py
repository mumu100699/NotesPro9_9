"""
======================
Author:cc
Time:2023/8/29 14:34
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
from parameterized import parameterized


class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase01_major(self):
        """获取首页便签列表，主流程校验"""
        info('获取首页便签')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }
        start_index = 0
        userid = 1145973490
        rows = 50
        get_userid_url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        get_userid_res = requests.get(url=get_userid_url, headers=headers)
        self.assertEqual(200, get_userid_res.status_code)   # 状态断言
        expect_output = {'responseTime': int, 'webNotes': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()

