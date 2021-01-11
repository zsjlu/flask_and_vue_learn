# -*- coding: utf-8 -*-
# @Time    :2021/1/10 15:55
# @Author  :robot_zsj
# @File    :test_backend.py
from datetime import datetime

import requests

testcase_url = 'http://127.0.0.1:5000/testcase'
testtask_url = 'http://127.0.0.1:5000/task'


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


def test_task():
    r = requests.post(
        testtask_url,
        json={
            'testcases': [1, 2, 3]
        }
    )
    assert r.json()['msg'] == 'ok'


def test_get_task():
    r = requests.get(
        testtask_url,
        params={'id': '1'}
    )
    assert r.json()['msg'] == 'ok'


def test_put_task_to_jenkins():
    r = requests.put(
        testtask_url,
        json={
            'id': '2'
        }
    )
    assert r.status_code == 200
    assert r.json()['msg'] == 'ok'
