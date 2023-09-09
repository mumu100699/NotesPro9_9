"""
======================
Author:cc
Time:2023/9/6 10:53
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
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    # path = apiConfig['NoteGroup']['path']
    # host = envConfig['host']
    # url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 =envConfig['user_id_2']
    apiRe = ApiRe()

    def setUp(self) -> None:
        step("初始化，清空用户便签数据")
        clear_notes_method(self.user_id, self.sid)
        clear_notes_method(self.user_id2, self.sid2)

    def testCase05_handles(self):  # handles校验
        """校验不同的操作对象，便签数据存在其他用户，只返回该用户正常的便签数据"""
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        info('创建用户2的便签数据')
        user2_note_id = generate_notes(num=1, sid=self.sid2, user_id=self.user_id2)

        info("获取首页便签数据")
        start_index = 0
        userid = 1145973490
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(200, res.status_code)  # 状态断言
        # print(len(res.json()['webNotes']))
        self.assertEqual(1, len(res.json()['webNotes']))
        self.assertEqual(user1_note_id[0], res.json()['webNotes'][0]['noteId'])

    def testCase06_handles(self):  # handles校验
        """用户存在不同的便签数据校验，2条便签数据"""
        step("创建用户1的便签数据，2条")
        user1_note_id = generate_notes(num=2, sid=self.sid, user_id=self.user_id)

        step("获取首页便签数据")
        start_index = 0
        userid = 1145973490
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(200, res.status_code)  # 状态断言
        # print(len(res.json()['webNotes']))
        self.assertEqual(2, len(res.json()['webNotes']))

    def testCase07_handles(self):  # handles校验
        """用户存在不同的便签数据校验，0条便签数据"""
        step("创建用户1的便签数据，0条")
        # user1_note_id = generate_notes(num=2, sid=self.sid, user_id=self.user_id)

        step("获取首页便签数据")
        start_index = 0
        userid = 1145973490
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(200, res.status_code)  # 状态断言
        # print(len(res.json()['webNotes']))
        self.assertEqual(0, len(res.json()['webNotes']))  # 返回空列表

    def testCase08_handles(self):  # handles校验
        """越权场景校验，用户1查询用户2的便签数据"""
        step("创建用户1的便签数据，1条")
        user2_note_id = generate_notes(num=1, sid=self.sid2, user_id=self.user_id2)

        step("获取首页便签数据")
        start_index = 0
        userid = self.user_id2
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(412, res.status_code)  # 状态断言
        # print(len(res.json()['webNotes']))
        # self.assertEqual(1, len(res.json()['webNotes']))  # 返回空列表

        expect_output = {'errorCode': -1011, 'errorMsg': 'user change!'}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()


