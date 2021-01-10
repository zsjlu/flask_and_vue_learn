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

class TestCase_(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    steps = db.Column(db.String(1024), nullable=True)
    #
    # testserver_id = db.Column(db.Integer, db.ForeignKey('testserver_.id'), nullable=True)
    # testserver = db.relationship('TestService_', backref=db.backref('testcase_', lazy=True))

    def __repr__(self):
        return '<TestCase %r>' % self.name

class TestCaseService(Resource):
    def get(self):
        """
        测试用例的浏览 /testcase.json /testcase.json?id=1
        查询全部、通过的查询单条、通过负整数删除单条记录
        :return:
        """
        # 获取参数，通过id筛选
        req = request.args
        var_args = req['id'] if "id" in req else ''
        if var_args:
            if int(var_args) < 0:
                var_args = -int(var_args)
                testcases: List[TestCase_] = TestCase_.query.filter(TestCase_.id == str(var_args)).first()
                db.session.delete(testcases)
                db.session.commit()
            else:
                testcases: List[TestCase_] = TestCase_.query.filter(TestCase_.id == var_args)
                res = [{
                    'id': testcase.id,
                    'name': testcase.name,
                    'description': testcase.description,
                    'steps': json.loads(testcase.steps)
                } for testcase in testcases]
                return {
                    'body': res
                }
        else:
            testcases: List[TestCase_] = TestCase_.query.all()
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
        req = request.json
        var_args = req['id'] if "id" in req else ''
        if var_args:
            # 更新方法方法一
            TestCase_.query.filter_by(id=var_args).update({
                'name': req['name'],
                'description': req['description'],
                'steps': json.dumps(req['steps'])
            })
            # 更新方法方法二
            # testcases: List[TestCase] = TestCase.query.filter_by(id=var_args)
            # testcases.name = req['name']
            # testcases.description = req['description']
            # testcases.steps = json.dumps(req['steps']
            db.session.commit()
        else:
            testcase=TestCase_(
                name=request.json.get('name'),
                description=request.json.get('description'),
                steps=json.dumps(request.json.get('steps'))
                )
            db.session.add(testcase)
            db.session.commit()
        return 'ok'

# class TestService_(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     servicename = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(120), nullable=True)
#     steps = db.Column(db.String(1024), nullable=True)
#
#     def __repr__(self):
#         return '<TestService_ %r>' % self.name

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