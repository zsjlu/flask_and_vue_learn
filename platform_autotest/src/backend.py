# -*- coding: utf-8 -*-
# @Time    :2021/1/10 15:28
# @Author  :robot_zsj
# @File    :backend.py
import json
from typing import List

from flask import Flask, escape, request
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# app实例
from jenkinsapi.jenkins import Jenkins

app = Flask(__name__)
CORS(app)
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
# app.config['jenkins'] = Jenkins(
#     'http://192.168.0.245:8080/',
#     username='admin',
#     password='118705f9853e42af406f8f8a2146681e43'
#     # password='admin'
# )


@app.route('/')
def hello_world():
    return 'Hello, World!'


class TestService(db.Model):
    __tablename__ = 'testservice'
    id = db.Column(db.Integer, primary_key=True)
    servicename = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('testcase.id'), nullable=False)
    testcase = db.relationship('TestCase', backref=db.backref('testservice', lazy=True))

    def __repr__(self):
        return '<data_object TestService>'


class TestCase(db.Model):
    __tablename__ = 'testcase'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    steps = db.Column(db.String(1024), nullable=True)

    # task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    # task = db.relationship('Task', backref=db.backref('testcase', lazy=True))

    def __repr__(self):
        return '<data_object TestCase>'


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    testcases = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return '<data_object Task>'


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
                testcases: List[TestCase] = TestCase.query.filter(TestCase.id == str(var_args)).first()
                db.session.delete(testcases)
                db.session.commit()
            else:
                testcases: List[TestCase] = TestCase.query.filter(TestCase.id == var_args)
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
        req = request.json
        var_args = req['id'] if "id" in req else ''
        if var_args:
            # 更新方法方法一
            TestCase.query.filter_by(id=var_args).update({
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
            testcase = TestCase(
                name=request.json.get('name'),
                description=request.json.get('description'),
                steps=json.dumps(request.json.get('steps'))
            )
            db.session.add(testcase)
            db.session.commit()
        return 'ok'


class TaskService(Resource):
    def get(self):
        id = request.args.get('id')
        if id:
            task = Task.query.filter_by(id=id).first()
            return {
                'msg': 'ok',
                'body': json.loads(task.testcases)
            }
        else:
            tasks = Task.query.all()
            return {
                'msg': 'ok',
                'body': [json.loads(task.testcases) for task in tasks]
            }

    def post(self):
        """
        上传测试用例，更新用例 /task.json {'testcases': [1,2,3,4]}
        :return:
        """
        testcase_id = request.json.get('testcases')
        task = Task(testcases=json.dumps(testcase_id))
        print(task)
        db.session.add(task)
        db.session.commit()
        return {'msg': 'ok'}

    def put(self):
        id = request.json.get('id')
        if id:
            task = Task.query.filter_by(id=id).first()
            testcases_info = []
            # 通过task数据对象，获取对应的testcases_id；再通过testcase_id获取testcase表中的数据信息
            for id in json.loads(task.testcases):
                testcase = TestCase.query.filter_by(id=id).first()
                case_info = {
                    'name': testcase.name,
                    'steps': testcase.steps
                }
                testcases_info.append(case_info)

            task_info = {
                'id': task.id,
                'testcases': testcases_info
            }
            jenkins: Jenkins = app.config['jenkins']
            jenkins['flask_to_jenkins'].invoke(
                build_params={
                    'task': json.dumps(task_info)
                })
            return {
                'msg': 'ok'
            }


class ReportService(Resource):
    def get(self):
        """
        通过jenkins构建后操作，及jenkinsapi获取构建任务后的信息
        :return:
        """
        pass



api.add_resource(TestCaseService, '/testcase')
api.add_resource(TaskService, '/task')
api.add_resource(ReportService, '/report')

if __name__ == '__main__':
    app.run(debug=True)
