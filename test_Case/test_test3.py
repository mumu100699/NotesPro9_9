"""
======================
Author:cc
Time:2023/8/30 13:54
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized  # 参数化实现


class TestPro(unittest.TestCase):
    must_key = ([{'key': 'noteId', 'code': 500}], [{'key': 'title', 'code': 500}])  # 字典参数化的实现

    # def setUp(self):  # 数据的初始化，清空用户数据，登录
    #     print('setup')  # 怎么保障用例独立性

    # def tearDown(self):
    #     print('tearDown')
    #
    # @classmethod
    # def setUpClass(cls) -> None:  # 类级别的初始化
    #     print('setUpclass')

    def test_content01(self):
        """上传/更新便签内容主流程"""
        print('前置步骤：上传便签信息主体')
        url = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'  # 上传/更新便签信息主体
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = requests.post(url=url, headers=headers, json=body)
        # self.assertTrue(res.status_code == 200, msg='错误')  # 校验状态码
        infoVersion = res.json()['infoVersion']
        print(res.status_code)
        print(res.json())
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        print('上传便签内容')

        get_userid_url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }

        title = str(int(time.time() * 1000)) + '_title'
        summary = str(int(time.time() * 1000)) + '_summary'
        body = str(int(time.time() * 1000)) + '_body'

        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': body,
            'localContentVersion': infoVersion,
            'BodyType': 0
        }

        get_userid_res = requests.post(url=get_userid_url, headers=headers, json=body)
        print(get_userid_res.status_code)
        print(get_userid_res.json())
        self.assertEqual(200, get_userid_res.status_code)
        expect_output = {'responseTime': int, 'contentVersion': 1, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()

    @parameterized.expand(must_key)  # 所以执行的时候要从类执行，class
    def test_content02(self, dic):
        """上传/更新便签内容主流程，必填项校验noteId"""
        print(f'必填项校验的字段{dic}')
        print('前置步骤：上传便签信息主体')
        url = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'  # 上传/更新便签信息主体
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = requests.post(url=url, headers=headers, json=body)
        # self.assertTrue(res.status_code == 200, msg='错误')  # 校验状态码
        infoVersion = res.json()['infoVersion']
        print(res.status_code)
        print(res.json())
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        print('上传便签内容')

        get_userid_url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }

        title = str(int(time.time() * 1000)) + '_title'
        summary = str(int(time.time() * 1000)) + '_summary'
        body = str(int(time.time() * 1000)) + '_body'

        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': body,
            'localContentVersion': infoVersion,
            'BodyType': 0
        }
        body.pop(dic['key'])  # 必填项校验，去掉这个，会报错

        get_userid_res = requests.post(url=get_userid_url, headers=headers, json=body)
        print(get_userid_res.status_code)
        print(get_userid_res.json())
        self.assertEqual(dic['code'], get_userid_res.status_code)
        expect_output = {'responseTime': int, 'contentVersion': 1, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()
