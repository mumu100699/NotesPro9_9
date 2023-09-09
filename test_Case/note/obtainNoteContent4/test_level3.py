"""
======================
Author:cc
Time:2023/9/8 10:44
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
from parameterized import parameterized  # 参数化实现
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteSvrSetNoteGetContent']['path']
    host = envConfig['host']
    url = host + path  # # 上传/更新便签信息主体
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    # def setUp(self) -> None:
    #     step("初始化，清空用户便签数据")
    #     clear_notes_method(self.user_id, self.sid)
    #     clear_notes_method(self.user_id2, self.sid2)

    def test06_handles(self):
        """获取便签内容，检验用户2获取用户1的便签内容"""
        info('获取用户1的便签内容')
        start_index = 0  # 验证为空，正确的是start_index = 0
        userid = self.user_id
        rows = 50
        url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
        res_1 = self.apiRe.note_get_path(url, self.user_id, self.sid)
        self.assertEqual(200, res_1.status_code)  # 状态断言
        aa = res_1.json()['webNotes']
        note_ids = []
        for i in aa:
            note_ids.append(i['noteId'])
        body = {
            'noteIds': note_ids
        }

        info('用户2获取用户1便签的内容')
        res = self.apiRe.note_post(self.url, self.user_id2, self.sid2, body)
        self.assertEqual(500, res.status_code)
        expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()


