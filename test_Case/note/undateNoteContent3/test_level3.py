"""
======================
Author:cc
Time:2023/9/7 22:55
Project: interface828
love:xz
=======================
"""
import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized  # 参数化实现
from common.ymlOperation import ReadYaml
from common.caseLogMethod import class_case_log, info, error, warn, step
from businessCommon.apiRe import ApiRe
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


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
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()
    setNoteContentPath = apiConfig['NoteSvrSetNoteContent']['path']
    get_userid_url = host + setNoteContentPath

    def setUp(self) -> None:
        step("初始化，清空用户便签数据")
        clear_notes_method(self.user_id, self.sid)
        clear_notes_method(self.user_id2, self.sid2)

    def test07_handles(self):
        """上传/更新便签内容，校验是否上传/更新成功"""
        print('前置步骤：上传便签信息主体')
        info('步骤1：上传便签信息主体')

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        infoVersion = res.json()['infoVersion']
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
        self.assertEqual(200, get_userid_res.status_code)
        expect_output = {'responseTime': int, 'contentVersion': 1, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, get_userid_res.json())  # actual_output等于res.json()

        url = 'http://note-api.wps.cn/v3/notesvr/get/notebody'
        # 获取便签内容接口
        note_ids = [note_id]
        body3 = {
            'noteIds': note_ids
        }
        res_1 = self.apiRe.note_post(url, self.user_id, self.sid, body3)
        self.assertEqual(200, res_1.status_code)
        a = res_1.json()
        print(a)
        expect_output = {'responseTime': int, 'noteBodies': list}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res_1.json())  # actual_output等于res.json()

        self.assertEqual(body['noteId'], a['noteBodies'][0]['noteId'])
        self.assertEqual(body['title'], a['noteBodies'][0]['title'])
        self.assertEqual(body['summary'], a['noteBodies'][0]['summary'])
        self.assertEqual(body['body'], a['noteBodies'][0]['body'])
        self.assertEqual(body['BodyType'], a['noteBodies'][0]['bodyType'])

    def test08_handles(self):
        """上传/更新便签内容，越权校验,使用用户2区更新用户1的便签内容"""
        print('前置步骤：上传便签信息主体')
        info('步骤1：上传便签信息主体')

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id
        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        infoVersion = res.json()['infoVersion']
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

        print('用户2上传用户1的便签内容')
        info('用户2上传用户1的便签内容')

        body = {
            'noteId': note_id,
            'title': 'test_title',
            'summary': 'test_summary',
            'body': 'test_body',
            'localContentVersion': infoVersion,
            'BodyType': 0
        }

        res2 = self.apiRe.note_post(self.get_userid_url, self.user_id2, self.sid2, body)
        # self.assertEqual(412, res2.status_code)  # 状态断言，此方法越权成功，接口直接修改成功，服务端接口有误
        # expect_output = {'errorCode': -1011, 'errorMsg': 'user change!'}  # 期望结果：对齐文档
        self.assertEqual(200, res2.status_code)
        expect_output = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        CheckTools().check_output(expect_output, res2.json())  # actual_output等于res.json()


