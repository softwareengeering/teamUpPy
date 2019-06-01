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
    print ('create successful')


@app.route('/class_join', methods=['POST', 'GET'])
def class_join():
    # get: class_invite_id,  stu_id
    #return :none
    print('>>>>in class join')
    data = to_Data()
    #theClass = Class.query.filter_by(openId=data['stu_id']).all()
    newMember = ClassHasStu( class_id = data['class_invite_id'], user_id = data['stu_id'])
    db.session.add(newMember)
    db.session.commit()
    resJson = {}
    if newMember:
        print('添加成功')
        resJson['state'] = 1
        resJson['info'] = '班级创建创建成功！'
        resJson['class_id'] = data['class_invite_id']
    else:
        resJson['state'] = 0
        resJson['info'] = '班级创建失败。'

    return jsonify(resJson)




@app.route('/class_create2', methods=['POST', 'GET'])
def class_create2():
    #get:
    # 'class_id'
    # 'class_name'
    # 'class_teacher'
    # 'team_size'
    # 'class_intro'
    # 'class_creater'
    # 'clss_pwd'
    # return:
    # state, info, creater id(string),

    print('>>>>>in class_create2')
    data = to_Data()
    resJson = {}
    if data['class_pwd'] == None :
        print("pwd is None")
        resJson['state'] = 0
        resJson['info'] = "密码不能为空，请输入密码！"
        return jsonify(resJson)
    if data['team_size'] == None :
        print("limit is None")
        resJson['state'] = 0
        resJson['info'] = "每队上限不能为空，请输入每队上限！"
        return jsonify(resJson)
    if isinstance(data['team_size'],int):
        print("limit is not num")
        resJson['state'] = 0
        resJson['info'] = "每队上限必须为数字，请重新输入！"
        return jsonify(resJson)
    if data['class_name'] == None :
        print("name is None")
        resJson['state'] = 0
        resJson['info'] = "班级名字不能为空，请输入班级名字！"
        return jsonify(resJson)

    newClass = Class(id=data['class_id'], name=data['class_name'], teacher=data['class_teacher'],
                     limit=data['team_size'], intro=data['class_intro'], creater=str(data['class_creater'])
                     ,pwd=data['class_pwd']
                     )
    db.session.add(newClass)
    db.session.commit()
    if newClass:
        print('添加成功')
        resJson['state'] = 1
        resJson['info'] = '班级创建创建成功！'
        resJson['createrId'] = str(data['class_creater'])
    else:
        resJson['state'] = 0
        resJson['info'] = '班级创建失败。'

    return jsonify(resJson)


@app.route('/class_create1', methods=['POST', 'GET'])
def class_create1():
    #get: OPEN_ID of creater,
    #return : max num of classes
    print('>>>>>in class create 1')
    resJson = {}
    maxId = db.session.query(func.max(Class.id)).one()
    print( maxId[0])
    flag = 0
    if maxId[0] != None:
        print('>>>maxID exist')
        resJson['class_last_id'] = int(maxId[0])
        resJson['state'] = 1
        resJson['info'] = str('成功！')
        flag = 1
    else:
        print('>>>maxID not exist')
        resJson['class_last_id'] = 0
        resJson['state'] = 1
        resJson['info'] = str('创建成功！')
        flag = 1
    if flag == 0:
        resJson['state'] = 0
        resJson['info'] = str('遇到了问题嗷嗷')

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
        resJson['user_name'] = userList[0]['name']
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

    userTmp = {}
    for x in Userres:
        userTmp['student_info'] = {'name':x.name , 'id':x.sno  }
        userList.append(userTmp)
    print(userList)
    resJson = {}
    if Userres != []:
        resJson['student_info'] = userTmp['student_info']

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

@app.route('/modifyName', methods=['POST','GET'])
def modifyName():
    print ( 'in modifing name')
    data = to_Data()
    print (data)

    OK = Users.query.filter_by(openId =data['open_id']).update({'name':data['student_name'], 'sno':data['student_id'] })
    resJson = {}
    if OK:
        db.session.commit()
        resJson['state'] = 1
        resJson['info'] = 'success'
    else:
        resJson['state'] = 0
        resJson['info'] = 'sth wrong'

    return jsonify(resJson)
@app.route('/')
def index():
    #return render_template('index.html')
    return ("首页")




if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 80) # 若要配置在服务器上
    app.run()