"""
======================
Author:cc
Time:2023/8/31 23:18
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
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['ViewRecycle']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()

    def testCase01_major(self):
        """查看回收站下便签列表，主流程校验"""
        info('查看回收站下便签列表')

        startIndex = 0
        rows = 10
        aa = self.url.format('', userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)

        res = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'responseTime': int, 'webNotes': list}
        CheckTools().check_output(expect_output, res.json())


