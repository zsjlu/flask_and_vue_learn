# -*- coding: utf-8 -*-
# @Time    :2021/1/10 17:19
# @Author  :robot_zsj
# @File    :test.db.py
from platform_autotest.src.backend import db


def test_create_table():
    db.create_all()