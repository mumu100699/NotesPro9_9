"""
======================
Author:cc
Time:2023/8/30 22:39
Project: interface828
love:xz
=======================
"""
import requests
from common.caseLogMethod import info
import json


class ApiRe:
    @staticmethod  # 静态方法
    def note_post(url, user_id, sid, body):
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(user_id),
            'cookie': f'wps_sid={sid}'
        }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        res = requests.post(url=url, headers=headers, json=body)

        info(f'res code:{res.status_code}')
        info(f'res body:{res.text}')

        return res

    @staticmethod
    def note_get(url, user_id, sid, params):
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(user_id),
            'cookie': f'wps_sid={sid}'
        }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        res = requests.get(url=url, headers=headers, params=params)

        info(f'res code:{res.status_code}')
        info(f'res body:{res.text}')

        return res

    @staticmethod
    def note_patch(url, user_id, sid, body):
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(user_id),
            'cookie': f'wps_sid={sid}'
        }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        res = requests.patch(url=url, headers=headers, json=body)

        info(f'res code:{res.status_code}')
        info(f'res body:{res.text}')

        return res

    @staticmethod
    def note_get_path(url, user_id, sid):
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(user_id),
            'cookie': f'wps_sid={sid}'
        }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        res = requests.get(url=url, headers=headers)

        info(f'res code:{res.status_code}')
        info(f'res body:{res.text}')

        return res
