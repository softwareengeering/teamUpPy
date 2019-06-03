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

@app.route('/team_create2', methods=['POST', 'GET'])
def team_create2():
    '''
    get:
    'leader_name': e.detail.value.leader_name,
    'team_info': e.detail.value.info,
    'team_invitors': this.data.invitors,
    'team_id': this.data.team.id,
    'team_sup': this.data.team.sup,
    return: state, info
    '''
    print(">>>>>in  team create 2")


@app.route('/team_create1', methods=['POST', 'GET'])
def team_create1():
    ''''''
    # get: class_id, student_id
    # return:
    # class_info: {id: 69321, name: "面向对象程序设计", sup: 5, teams_count: 5,
    #              single_list: ["张一一", "张二二", "张三三", "张五五", "张一一", "张二二", "张三三", "张五五", "张一一", "张二二"], last_team_id: 5},
    # team: {id: 321, sup: 5, info: "在此可输入队伍名，队伍简介，队员要求等信息"},
    # leader_name: "张一一",
    # invitors: []
    # info
    # state
    print(">>>>int team create 1")
    data = to_Data()
    resJson = {}
    theClass = Class.query.filter_by(id = data['class_id']).one()
    leader = Users.query.filter_by(openId = data['student_id']).one()
    if theClass is None or leader is None:
        resJson['state'] = 0
        resJson['info'] = '出错了嗷嗷嗷'
        return jsonify(resJson)
    print("the class is: ", theClass)
    resJson['leader_name'] = leader.name
    classInfo = {}
    classInfo['id'] = int(theClass.id)
    classInfo['name'] = theClass.name
    classInfo['sup'] = theClass.limit
    teamsIn = Team.query.filter_by(class_id = data['class_id']).count()
    classInfo['teams_count'] = int(teamsIn)
    stuList = []
    stu = ClassHasStu.query.filter_by(class_id = data['class_id']).all()
    for s in stu:
        print("user id in the class: ", s.user_id)
        if s.user_id != data['student_id']:
            stuName = Users.query.filter_by(openId = s.user_id).one()
            if stuName:
                stuList.append(stuName.name)
    classInfo['single_list'] = stuList
    print("class id: ", classInfo['id'])
    print("class name: ", classInfo['name'])
    print("class sup: ", classInfo['sup'])
    print("class teams count: ", classInfo['teams_count'])

    resJson['class_info'] = classInfo

    teamInfo = {}
    teamID = db.session.query(func.max(Team.id)).one()
    teamInfo['id'] = int(teamID[0])+1
    #teamInfo['team'] = int(teamID[0]) + 1
    #leaderName = Users.query.filter_by(openId = data['student_id']).one()
    #teamInfo['leader_name'] = leaderName.name
    teamInfo['sup'] = theClass.limit
    teamInfo['info'] = '在此可输入队伍名，队伍简介，队员要求等信息'
    resJson['team'] = teamInfo
    #print("team team: ", teamInfo['team'])
    #print("team leader_name: ", teamInfo['leader_name'])
    print("team sup: ", teamInfo['sup'])
    print("team id: ", teamInfo['id'])
    if resJson['team'] is not None and resJson['class_info']is not None :
        resJson['state'] = 1
        resJson['info'] = "队伍创建成功！"
        print("信息返回成功嗷嗷")
    else:
        resJson['state'] = 0
        resJson['info'] = "队伍创建遇到了问题嗷嗷 哭哭"
        print("team list出错了 哭哭")

    return jsonify(resJson)




@app.route('/class_list', methods=['POST', 'GET'])
def class_list():
    # get: student_id
    # return:
    '''
    user: { name: '啊啊啊', id: 2016, fname: '啊' },
    class_data: [{ id: 1, name: "算法", teacher: "刘青", student_numbers: 56, team_numbers: 5 },
    { id: 2, name: "软件工程", teacher: "刘青", student_numbers: 72,team_numbers: 9 }],
    info,
    state
    '''
    print('>>>>>int class list')
    data = to_Data()
    resJosn = {}
    classes = ClassHasStu.query.filter_by( user_id=data['student_id']).distinct().all()
    print(classes)
    i = 0
    flag1 = 0
    res = []
    for c in classes :
        classx = {}
        classx['id'] = str(i+1)
        i += 1
        #print("class id: ")
        className = Class.query.filter_by(id=c.class_id).distinct().all()
        print("class: ", className)
        print('name: ', className[0].name, '\nteacher: ', className[0].teacher, '\nlimit: ', className[0].limit)
        classx['name'] = className[0].name
        classx['teacher'] = className[0].teacher
        classx['student_numbers'] = int(className[0].limit)
        teams = Team.query.filter_by(class_id = c.id).count()
        print('team num: ', teams)
        classx['team_numbers'] = int(teams)
        res.append(classx)
        flag1 = 1
    resJosn['classes'] = res

    resUser = {}
    userName = Users.query.filter_by(openId = data['student_id']).all()
    print(userName[0])
    resUser['name'] = userName[0].name
    resUser['id'] = userName[0].sno
    resUser['fname'] = userName[0].name[0:1]

    flag2 = 0
    if resUser is not None:
        resJosn['user'] = resUser
        flag2 = 1

    if flag1 ==1 and flag2 ==1 :
        resJosn['state'] = 1
        resJosn['info'] = '班级列表获取成功！(＾－＾)V'
    else:
        resJosn['state'] = 0
        resJosn['info'] = '遇到了错误嗷嗷嗷'
    print(resJosn)
    print("班级列表获取成功！(＾－＾)V")
    return jsonify(resJosn)



@app.route('/class_join', methods=['POST', 'GET'])
def class_join():
    # get: class_invite_id,  stu_id
    #return :none
    print('>>>>in class join')
    data = to_Data()
    resJson = {}
    theClass = Class.query.filter_by(id=data['class_invite_id']).all()
    notIn = ClassHasStu.query.filter (ClassHasStu.class_id==data['class_invite_id'] , ClassHasStu.user_id==data['stu_id'])
    if theClass[0] is None :
        print('班级不存在')
        resJson['state'] = 0
        resJson['info'] = '邀请码输入错误，班级不存在嗷'
        return jsonify(resJson)
    if  notIn is not None :
        print('学生已在班级中')
        resJson['state'] = 0
        resJson['info'] = '你已经在该班级中了嗷'
        return jsonify(resJson)

    newMember = ClassHasStu( class_id = data['class_invite_id'], user_id = data['stu_id'])
    db.session.add(newMember)
    db.session.commit()
    if newMember:
        print('加入班级成功')
        resJson['state'] = 1
        resJson['info'] = '班级创建创建成功！'
        resJson['class_id'] = data['class_invite_id']
    else:
        print('加入班级失败嗷嗷')
        resJson['state'] = 0
        resJson['info'] = '加入班级遇到了点问题嗷嗷嗷'

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