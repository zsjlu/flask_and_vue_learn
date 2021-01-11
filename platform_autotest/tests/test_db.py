# -*- coding: utf-8 -*-
# @Time    :2021/1/10 17:19
# @Author  :robot_zsj
# @File    :test.db.py
from jenkinsapi.jenkins import Jenkins

from platform_autotest.src.backend import db


def test_create_table():
    db.create_all()

def test_jenkins():
    jenkins = Jenkins(
        'http://192.168.0.245:8080/',
        username='admin',
        password='118705f9853e42af406f8f8a2146681e43'
        # password='admin'
    )
    print(jenkins.keys())
    res = jenkins['flask_to_jenkins'].invoke(build_params={'testcases': '123'})
    print(res)