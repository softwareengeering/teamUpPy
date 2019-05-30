from flask import Flask, render_template, request, make_response, send_file ,jsonify
from models import Admin, Student, Project, Users , Team , Class , ClassHasStu
from exts import db
import config, os
from methods import get_rand, get_Info, to_Data, to_List, to_Json, new_avatar_name, create_xlsx
from flask_cors import *
from sqlalchemy import func

app = Flask(__name__)
CORS(app, supports_credentials = True) # 解决跨域问题

app.config.from_object(config)
db.init_app(app)


url = "http://127.0.0.1:5000/"
@app.before_first_request
def init_db():
    print ('>>>>>>>>creating DB...')
    db.create_all()

@app.route('/class_create2', methods=['POST', 'GET'])
def class_create2():
    #get:
    # 'class_id'
    # 'class_name'
    # 'class_teacher'
    # 'team_size'
    # 'class_intro'
    # 'class_creater'
    ## password
    # return:
    # state, info, max class num, creater id,

    print('in class_create')
    data = to_Data()
    newClass = Class(id=data['class_id'], name=data['calss_name'], teacher=data['class_teacher'],
                     limit=data['team_size'], intro=data['class_intro'], creater=str(data['class_creater'])
                     #,pwd=data['password']
                     )
    db.session.add(newClass)
    db.session.commit()
    resJson = {}
    if newClass:
        print('添加成功')
        resJson['state'] = 1
        resJson['info'] = '班级创建创建成功！'
    else:
        resJson['state'] = 0
        resJson['info'] = '班级创建失败。'
    return jsonify(resJson)


@app.route('/class_create1', methods=['POST', 'GET'])
def class_create1():
    #get: OPEN_ID of creater,
    #return : max num of classes
    resJson = {}
    maxId = db.session.query(func.max(Class.id)).one()
    if maxId != None:
        resJson['class_last_id'] = int(maxId)
        resJson['state'] = 1
        resJson['info'] = '成功！'
    else:
        resJson['class_last_id'] = 0
        resJson['state'] = 1
        resJson['info'] = '成功！'
    return jsonify(resJson)


        # "http://127.0.0.1:5000/test"
@app.route('/login',methods=['POST','GET'])
def test():
    print( 'in login ....')
    data = to_Data()
    Userres = Users.query.filter_by(openId=data['open_id']).all()
    userList = []
    print (Userres)
    for x in Userres:
        userTmp = {}
        userTmp['id'] =x.id
        userTmp['name'] = x.name
        userTmp['openId'] = x.openId
        userTmp['sno'] = x.sno
        userList.append(userTmp)
    print (userList)
    resJson = {}
    if userList != []:
        print ( 'NotNone')
        resJson['student_id'] = userList[0]['sno']
        resJson['state'] = 1
    else:
        print('None')
        newUser = Users(id=str(10000+ get_rand()), name = '新同学', openId=data['open_id'] , Sno = '1000000')
        db.session.add(newUser)
        db.session.commit()
        print ('添加成功')
        resJson['student_id'] = None
        resJson['state'] = 0
    resJson['info'] = 'success'
    return jsonify(resJson)


@app.route('/register',methods=['POST','GET'])
def register():
    print( 'in register ....')
    data = to_Data()
    OK = Users.query.filter_by(openId =data['open_id']).update({'name':data['student_name'], 'sno':data['student_id'] })
    resJson = {}
    if OK:
        db.session.commit()
        resJson['state'] = 1
    else:
        resJson['state'] = 0

    return jsonify(resJson)

# /get_user_info
@app.route('/get_user_info', methods=['POST','GET'])
def getUserInfo():
    print ('>>>>>> in get_user_info .... ')
    data = to_Data()
    Userres = Users.query.filter_by(openId=data['open_id']).all()
    userList = []

    for x in Userres:
        userTmp = {}
        # userTmp['student_info'] = {'':  , '':  }
    print(userList)
    resJson = {}
    if userList != []:

        resJson['state'] = 1
    else:
        resJson['state'] = 0

    return jsonify(resJson)

@app.route('/classList', methods=['POST','GET'])
def classList():
    # data = to_Data()
    # print (data)
    classListData = {
        'state': 0,
        'student_info' : 'studentInfo',
        'classes' : 'classes'
    }
    return jsonify(classListData)

@app.route('/')
def index():
    #return render_template('index.html')
    return ("首页")




if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 80) # 若要配置在服务器上
    app.run()