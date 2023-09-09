"""
======================
Author:cc
Time:2023/9/7 11:04
Project: interface828
love:xz
=======================
"""
# 原始的写接口用例的写法
import unittest
import requests
import time

url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notegroup'
# 新增分组接口，第7
headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1145973490',
            'cookie': 'wps_sid=V02SUGGKho67jU5kKjCXDVTu_I1zflI00a30970d00444e2af2'
        }

group_id = str(int(time.time() * 1000)) + '_groupId'
group_name = str(int(time.time() * 1000)) + '_groupName'
body = {
    'groupId': group_id,
    'groupName': group_name
}
res = requests.post(url=url, headers=headers, json=body)
assert res.status_code == 200
assert 'responseTime' in res.json().keys()  # 验证返回
assert 'updateTime' in res.json().keys()  # 验证返回体是否在
assert type(res.json()['responseTime']) == int  # 验证返回体是否为int类型
assert type(res.json()['updateTime']) == int  # 验证返回体是否为int类型
assert len(res.json().keys()) == 2  # 验证返回体的长度是否为2

get_group_url = 'http://note-api.wps.cn' + '/v3/notesvr/get/notegroup'
# 获取分组列表的接口，第6，校验新增分组之后，数据源有没有在数据库里面。
body = {}
get_res = requests.post(url=get_group_url, headers=headers, json=body)
print(get_res.json())
print(get_res.status_code)
groupIds = []
groupNames = []
for i in get_res.json()['noteGroups']:
    groupIds.append(i['groupId'])
    groupNames.append(i['groupName'])
assert group_id in groupIds   # 校验前面生成的分组数据是否存在查询分组的列表里面
assert group_name in groupNames



