# -*- coding: utf-8 -*-
# @Time    :2021/1/10 15:28
# @Author  :robot_zsj
# @File    :backend.py
import json
from typing import List

from flask import Flask, escape, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


# app实例
app = Flask(__name__)

# restful实例
api = Api(app)

# sqlalchemy实例
# sqlilte
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/db.sqlite3'
# mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_vue:dcCf4nL@@47.115.163.10:3306/flask_vue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# fake db
app.config['db'] = []

@app.route('/')
def hello_world():
    return 'Hello, World!'

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    steps = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return '<TestCase %r>' % self.name

class TestCaseService(Resource):
    def get(self):
        """
        测试用例的浏览 /testcase.json /testcase.json?id=1
        :return:
        """
        print(TestCase.query.all())
        testcases: List[TestCase] = TestCase.query.all()
        res = [{
            'id': testcase.id,
            'name': testcase.name,
            'description': testcase.description,
            'steps': json.loads(testcase.steps)
        } for testcase in testcases]
        return {
            'body': res
        }

    def post(self):
        """
        上传用例，更新用例
        /testcase.json {'name': 'xx', 'description': 'xxx', 'steps':[]}
        :return:
        """
        testcase=TestCase(
            name=request.json.get('name'),
            description=request.json.get('description'),
            steps=json.dumps(request.json.get('steps'))
            )
        db.session.add(testcase)
        db.session.commit()
        return 'ok'

class TaskService(Resource):
    def get(self):
        pass

class ReportService(Resource):
    def get(self):
        pass

api.add_resource(TestCaseService, '/testcase')
api.add_resource(TaskService, '/task')
api.add_resource(ReportService, '/report')


if __name__ == '__main__':
    app.run(debug=True)