"""
======================
Author:cc
Time:2023/8/28 13:12
Project: python0731
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized  # 参数化实现
from common.ymlOperation import ReadYaml
from common.caseLogMethod import class_case_log, info, error, warn
from businessCommon.apiRe import ApiRe


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteSvrSetNoteInfo']['path']
    must_key = apiConfig['NoteSvrSetNoteInfo']['must_key']
    host = envConfig['host']
    url = host + path  # # 上传/更新便签信息主体
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    apiRe = ApiRe()
    setNoteContentPath = apiConfig['NoteSvrSetNoteContent']['path']
    get_userid_url = host + setNoteContentPath

    def test_content01(self):
        """上传/更新便签内容主流程"""
        print('前置步骤：上传便签信息主体')
        info('步骤1：上传便签信息主体')

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertTrue(res.status_code == 200, msg='错误')  # 校验状态码
        infoVersion = res.json()['infoVersion']
        # print(res.status_code)
        # print(res.json())
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        print('上传便签内容')
        info('上传便签内容')

        # get_userid_url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notecontent'

        body = {
            'noteId': note_id,
            'title': 'test_title',
            'summary': 'test_summary',
            'body': 'test_body',
            'localContentVersion': infoVersion,
            'BodyType': 0
        }

        get_userid_res = self.apiRe.note_post(self.get_userid_url, self.user_id, self.sid, body)
        # self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # print(get_userid_res.status_code)
        # print(get_userid_res.json())
        self.assertEqual(200, get_userid_res.status_code)
        expect_output = {'responseTime': int, 'contentVersion': 1, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()

    @parameterized.expand(must_key)  # 所以执行的时候要从类执行，class
    def test_content02(self, key):
        """上传/更新便签内容主流程，必填项校验noteId"""
        print(f'必填项校验的字段{key}')
        print('前置步骤：上传便签信息主体')
        info('用例2：必填项验证')

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertTrue(res.status_code == 200, msg='错误')  # 校验状态码
        infoVersion = res.json()['infoVersion']
        # print(res.status_code)
        # print(res.json())
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        print('上传便签内容')
        body = {
            'noteId': note_id,
            'title': 'test_title',
            'summary': 'test_summary',
            'body': 'test_body',
            'localContentVersion': infoVersion,
            'BodyType': 0
        }
        # body.pop(key)  # 必填项校验，去掉这个，会报错

        get_userid_res = self.apiRe.note_post(self.get_userid_url, self.user_id, self.sid, body)
        # print(get_userid_res.status_code)
        # print(get_userid_res.json())
        self.assertEqual(200, get_userid_res.status_code)
        expect_output = {'responseTime': int, 'contentVersion': 1, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()





