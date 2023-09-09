# 清空用户便签数据的方法
"""
======================
Author:cc
Time:2023/9/6 12:04
Project: interface828
love:xz
=======================
"""
import requests
from businessCommon.apiRe import ApiRe

apiRe = ApiRe()  # 实例化


def clear_notes_method(user_id, sid):
    # 获取用户首页便签的所有note_id
    start_index = 0
    userid = user_id
    rows = 100
    url = f'http://note-api.wps.cn/v3/notesvr/user/{str(userid)}/home/startindex/{str(start_index)}/rows/{str(rows)}/notes'
    res = apiRe.note_get_path(url, user_id, sid)
    print(res)
    note_ids = []
    for i in res.json()['webNotes']:
        note_id = i['noteId']
        note_ids.append(note_id)
    if len(note_ids) == 0:  # 如果用户没有便签数据，就不执行删除
        return

    for note_id in note_ids:
        # 删除所有便签数据
        delete_url = 'http://note-api.wps.cn/v3/notesvr/delete'
        body = {'noteId': note_id}
        apiRe.note_post(url=delete_url, user_id=user_id, sid=sid, body=body)

    # 获取回收站的所有便签noteID
    recycle_bin_url = f'http://note-api.wps.cn/v3/notesvr/user/{userid}/invalid/startindex/{0}/rows/{rows}/notes'
    recycle_res = apiRe.note_get_path(url=recycle_bin_url, user_id=user_id, sid=sid)  # post请求发起
    for i in recycle_res.json()['webNotes']:
        note_id = i['noteId']
        note_ids.append(note_id)

    # 清空回收站所有便签
    clear_recycle_notes_url = 'http://note-api.wps.cn/v3/notesvr/cleanrecyclebin'
    body = {
        'noteIds': note_ids
    }
    apiRe.note_post(url=clear_recycle_notes_url, user_id=user_id, sid=sid, body=body)  # post请求发起


if __name__ == '__main__':
    aa = clear_notes_method(1145973490, 'V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2')
    print(aa)

