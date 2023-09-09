"""
======================
Author:cc
Time:2023/9/7 17:09
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
    envConfig = ReadYaml().env_yaml()  # 读取yml文件的方法，实例化，设置一个变量envConfig接收
    print(envConfig)
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteSvrSetNoteInfo']['path']
    host = envConfig['host']
    url = host + path  # # 上传/更新便签信息主体
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def setUp(self) -> None:
        step("初始化，清空用户便签数据")
        clear_notes_method(self.user_id, self.sid)
        clear_notes_method(self.user_id2, self.sid2)

    # @unittest.skip('未完成')  # 暂时取消执行用例
    def test06_handles(self):  # 必须test开头命名
        """上传/更新便签主体，校验1条便签信息主体上传/更新成功"""
        info('上传/更新便签主体')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)

        info("获取首页便签数据")
        start_index = 0
        userid = 1145973490
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(200, res.status_code)  # 状态断言
        self.assertEqual(1, len(res.json()['webNotes']))
        self.assertEqual(user1_note_id[0], res.json()['webNotes'][0]['noteId'])

    def testCase07_handles(self):  # handles校验
        """越权场景校验，用户1查询用户2的便签数据"""
        step("用用户2查询列表")
        step("获取首页便签数据")
        start_index = 0
        userid = self.user_id2
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(412, res.status_code)  # 状态断言
        # print(len(res.json()['webNotes']))
        expect_output = {'errorCode': -1011, 'errorMsg': 'user change!'}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

