# -*- coding: utf-8 -*-
# @Time    :2021/1/10 15:55
# @Author  :robot_zsj
# @File    :test_backend.py
from datetime import datetime

import requests


def test_testcase_get():
    testcase_url = 'http://127.0.0.1:5000/testcase'
    r=requests.post(
        testcase_url,
        json={
            'name': f'case{datetime.now().isoformat()}',
            'description': 'description 1',
            'steps': ['1', '2', '3']
        }
                   )
    assert  r.status_code == 200

    r = requests.get(testcase_url)
    print(r.json())
    assert r.json()['body']
