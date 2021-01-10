# -*- coding: utf-8 -*-
# @Time    :2021/1/10 15:55
# @Author  :robot_zsj
# @File    :test_backend.py
from datetime import datetime

import requests

testcase_url = 'http://127.0.0.1:5000/testcase'

# 查询所有记录
def test_testcase_get():

    r = requests.get(testcase_url)
    print(r.json())
    assert r.json()['body']

# 通过id查询某条记录
def test_testcase_get_by_id():

    r = requests.get(testcase_url, params={'id': '1'})
    print(r.json())
    assert r.json()['body']

# 插入新输入，不含id字段表示新增
def test_testcase_post():
    r = requests.post(
        testcase_url,
        json={
            'name': f'case{datetime.now().isoformat()}',
            'description': 'description 1',
            'steps': ['1', '2', '3']
        }
    )
    assert r.status_code == 200

# 更新，json中有id关键字表示更新
def test_testcase_update():
    r = requests.post(
        testcase_url,
        json={
            'id': '1',
            'name': f'case{datetime.now().isoformat()}',
            'description': 'update',
            'steps': ['3', '2', '1']
        }
    )
    assert r.status_code == 200

# 删除某条记录，以符号开头表示删除
def test_testcase_delete():
    r = requests.get(
        testcase_url,
        params={'id': '-16'}
    )
    assert r.status_code == 200
