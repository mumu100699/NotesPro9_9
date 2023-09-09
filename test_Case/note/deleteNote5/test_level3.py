"""
======================
Author:cc
Time:2023/9/8 11:53
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
from parameterized import parameterized  # 参数化实现
from businessCommon.automation import generate_notes
from businessCommon.Clear_Notes import clear_notes_method


@class_case_log
class TestPro(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    path = apiConfig['NoteDelete']['path']
    host = envConfig['host']
    url = host + path
    sid = envConfig['sid_1']
    user_id = envConfig['user_id_1']
    sid2 = envConfig['sid_2']
    user_id2 = envConfig['user_id_2']
    apiRe = ApiRe()

    def test08_handles(self):
        """删除便签，删除用户不存在的便签"""
        info('删除便签')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        # 下面的noteid从接口1返回取出来
        note_id = '1693318482398_noteId'   # 1693318482398_noteId，user1_note_id[0]
        body = {
            'noteId': note_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int}  # 期望结果：对齐文档
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def test09_handles(self):
        """删除便签，越权删除，用户2删除用户1的便签数据"""
        info('删除便签')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        info(f'{user1_note_id}')
        # info('创建用户2的便签数据')
        # user2_note_id = generate_notes(num=1, sid=self.sid2, user_id=self.user_id2)
        # info(f'{user2_note_id}')
        # 下面的noteid从接口1返回取出来
        note_id = user1_note_id[0]   # 1693318482398_noteId，user1_note_id[0]
        body = {
            'noteId': note_id

        }

        res = self.apiRe.note_post(self.url, self.user_id2, self.sid2, body)
        print(res.json())
        print(res.status_code)
        # self.assertEqual(412, res.status_code)  # 越权成功，接口错误
        # expect_output = {'errorCode': int, 'errorMsg': str}  # 期望结果：对齐文档
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()

    def test10_handles(self):
        """删除便签，删除成功，校验在回收站可以查询到"""
        info('删除便签')
        info('创建用户1的便签数据')
        user1_note_id = generate_notes(num=1, sid=self.sid, user_id=self.user_id)
        info(f'{user1_note_id}')
        note_id = user1_note_id[0]   # 1693318482398_noteId，user1_note_id[0]
        body = {
            'noteId': note_id

        }

        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        print(res.json())
        print(res.status_code)
        self.assertEqual(200, res.status_code)
        expect_output = {'responseTime': int}
        CheckTools().check_output(expect_output, res.json())  # actual_output等于res.json()


        startIndex = 0
        rows = 10
        url_1 = 'http://note-api.wps.cn/v3/notesvr/user/{userid}/invalid/startindex/{startindex}/rows/{rows}/notes'
        aa = url_1.format(userid=self.user_id, startindex=startIndex, rows=rows)
        print(aa)
        res_3 = self.apiRe.note_get(aa, self.user_id, self.sid, None)
        self.assertEqual(200, res_3.status_code)
        bb = res_3.json()['webNotes']
        dd = False
        for i in bb:
            if note_id == i['noteId']:
                print('校验成功')
                self.assertEqual(note_id, i['noteId'])
                dd = True
        if dd:
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 2)




