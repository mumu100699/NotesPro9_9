"""
======================
Author:cc
Time:2023/8/31 19:17
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools


class TestPro(unittest.TestCase):
    def testCase_major(self):
        """获取分组列表"""
        url = 'http://note-api.wps.cn' + '/v3/notesvr/get/notegroup'
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'Cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }
        excludeInvalid = ''
        body = {
            'excludeInvalid': excludeInvalid

        }

        res = requests.post(url=url, headers=headers, json=body)
        self.assertEqual(200, res.status_code)
        print(res.json())
        expect_output = {'requestTime': int, 'noteGroups': list}
        CheckTools().check_output(expect_output, res.json())

