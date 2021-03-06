from flask import Flask, render_template, request, make_response, send_file ,jsonify
from models import *
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

@app.route('/team_delete', methods=['POST', 'GET'])
def team_delete():
    '''
    get:'class_id': app.globalData.class_id,
        'team_id': app.globalData.team_id,
    :return: state, info
    '''
    print('>>>in team delete')
    data = to_Data()
    flag = 1
    theTeam = Team.query.filter_by(id = data['team_id']).one()
    print('the team: ', theTeam)
    db.session.delete(theTeam)
    db.session.commit()

    stuRec = ClassHasStu.query.filter(ClassHasStu.class_id==data['class_id'],
                                      ClassHasStu.team_id == data['team_id']).all()
    for s in stuRec:
        s.team_id = None
    db.session.commit()

    if stuRec is None or theTeam is None:
        flag=0
    resJson = {}
    if flag == 0:
        resJson['state'] = 0
        resJson['info'] = 'sorry删除队伍失败'
        print('sorry删除队伍失败')
    else:
        resJson['state'] = 1
        resJson['info'] = '删除队伍成功'
        print('删除队伍成功,nice~')
    return  jsonify(resJson)


@app.route('/team_set2', methods=['POST', 'GET'])
def team_set2():
    '''
    get:  'leader_name': e.detail.value.leader_name,
        'team_info': e.detail.value.info,
        'team_members': this.data.team.members,
        'team_id': this.data.team.id,
        'class_id': this.data.class_id
    :return:
    state, info
    '''
    print('>>>>in team set 2')
    data = to_Data()
    resJson = {}
    theTeam = Team.query.filter_by(id=data['team_id']).one()
    if data['team_info'] :
        theTeam.msg = data['team_info']
    if data['leader_name']:
        newLeader = Users.query.filter_by(name=data['leader_name']).all()
        flag = 0
        for l in newLeader:
            leader1 = ClassHasStu.query.filter(ClassHasStu.user_id == l.openId,
                                               ClassHasStu.team_id == data['team_id'],
                                               ClassHasStu.class_id == data['class_id']).one()
            if leader1:
                theTeam.leader_id = leader1.user_id
                db.session.commit()
                flag = 1
                continue
        if flag == 0:
            resJson['state'] = 0
            resJson['info'] = '新队长名字错误或不在队伍中'
            return jsonify(resJson)


    theStuRec = ClassHasStu.query.filter(ClassHasStu.team_id == data['team_id'],
                                         ClassHasStu.class_id == data['class_id']).all()
    stuStillIn = []  # 记录还在队伍中的人的openId
    for s in data['team_members']:  #更改这些学生的ClassHasStu的记录 日
        sID = Users.query.filter_by(name = s).all()
        breakFlag = 0
        for si in sID:
            for sr in theStuRec:
                if si.openId == sr.user_id:
                    stuStillIn.append(si.openId)
                    break
                    breakFlag = 1
            if breakFlag==1:
                break
    for sr in theStuRec:
        if sr.user_id not in stuStillIn:
            sr.team_id = None
    db.session.commit()

    resJson['state'] = 1
    resJson['info'] = '队伍信息修改成功！'
    print('队伍信息修改成功! yeah')
    return jsonify(resJson)



@app.route('/team_set1', methods=['POST', 'GET'])
def team_set1():
    '''
    get:'class_id': app.globalData.class_id,
        'team_id': app.globalData.team_id,
    :return: state, team
    '''
    print('>>>in team set 1')
    data = to_Data()
    team = {}
    theClass = Class.query.filter_by(id=data['class_id']).one()
    theTeam = Team.query.filter_by(id=data['team_id']).one()
    team['id'] = data['team_id']
    print('the class: ', theClass)
    print('the team: ', theTeam)
    team['count'] = ClassHasStu.query.filter(ClassHasStu.class_id == data['class_id'],
                                             ClassHasStu.team_id == data['team_id']).count()
    team['sup'] = theClass.limit
    leaderN = Users.query.filter_by(openId=theTeam.leader_id).one()
    team['leader'] = leaderN.name
    team['info'] = theTeam.msg
    members = []
    stus = ClassHasStu.query.filter(ClassHasStu.class_id == data['class_id'],
                                    ClassHasStu.team_id == data['team_id']).all()
    for s in stus:
        stuName = Users.query.filter_by(openId=s.user_id).one()
        members.append(stuName.name)
    team['member'] = members
    print('team info: ', team)

    resJson = {}
    if team:
        resJson['team'] = team
        resJson['state'] = 1
        resJson['info'] = '队伍信息get成功'
        print('队伍信息get成功')
    else:
        resJson['state'] = 0
        resJson['info'] = '队伍信息get失败嗷嗷嗷'
        print('队伍信息get失败嗷嗷嗷')

    return jsonify(resJson)


@app.route('/team_more_join', methods=['POST', 'GET'])
def team_more_join():
    '''
    get:'class_id': app.globalData.class_id,
        'team_id': app.globalData.team_id,
        'student_id'
    :return:state
    '''
    print('>>>in team more join')
    data = to_Data()
    resJson = {}
    theTeam = ClassHasStu.query.filter(ClassHasStu.class_id==data['class_id'],
                                       ClassHasStu.team_id==data['team_id'],
                                       ClassHasStu.user_id==data['student_id']).all()
    print('the team: ', theTeam)
    if not theTeam :  #学生不在这个队伍中
        newRequest = JoinRequest(applicant_id=data['student_id'], team_id=data['team_id'])
        db.session.add(newRequest)
        db.session.commit()
        if newRequest:
            resJson['state'] = 1
            resJson['info'] = "申请成功 棒！"
            print('申请成功了yes！')
        else:
            resJson['state'] = 0
            resJson['info'] = "出了点问题。。"
            print('出了点问题 哭哭')
    else:
        resJson['state'] = 0
        resJson['info'] = "你已经在这个队伍中了嗷"
        print('这个傻逼学生已经在队伍中了，或者就是数据有问题了。')
    return jsonify(resJson)




@app.route('/team_more_set', methods=['POST', 'GET'])
def team_more_set():
    '''
    get:'student_id': app.globalData.student_id,
        'team_id':this.data.team.id
    :return: stete, confirm
    '''
    print('>>>>in team more set')
    data = to_Data()
    resJson = {}
    theTeam = Team.query.filter_by(id=data['team_id']).one()
    print('the team: ', theTeam)
    print('team leader: ', theTeam.leader_id )
    print('student id: ', data['student_id'])
    if theTeam.leader_id == data['student_id']:
        resJson['confirm'] = 1
        resJson['state'] = 1
    else:
        resJson['confirm'] = 0
        resJson['state'] = 1
    print(resJson)
    print('team more set 返回啦啦')
    return jsonify(resJson)


@app.route('/team_more', methods=['POST', 'GET'])
def team_more():
    '''get:team_id, class_id
    return: team_info: { id: 321, count: 3, sup: 5, leader: "张一一",
                    info: "这是一这是这是一个神秘的队伍", member: ["张一一", "张二二", "张三三"] }
    state ,
    '''
    print('>>>>>in team more onload')
    data = to_Data()
    team = {}
    theClass = Class.query.filter_by(id=data['class_id']).one()
    theTeam = Team.query.filter_by(id = data['team_id']).one()
    team['id'] = data['team_id']
    print('the class: ', theClass)
    print('the team: ', theTeam)
    team['count'] = ClassHasStu.query.filter(ClassHasStu.class_id == data['class_id'],
                                             ClassHasStu.team_id == data['team_id']).count()
    print(team)
    team['sup'] = theClass.limit
    leaderN = Users.query.filter_by(openId = theTeam.leader_id).one()
    team['leader'] = leaderN.name
    team['info'] = theTeam.msg
    members = []
    stus = ClassHasStu.query.filter(ClassHasStu.class_id == data['class_id'],
                                    ClassHasStu.team_id == data['team_id']).all()
    for s in stus:
        stuName = Users.query.filter_by(openId=s.user_id).one()
        members.append(stuName.name)
    team['member'] = members
    print('team info: ', team)

    resJson = {}
    if team:
        resJson['team_info'] = team
        resJson['state'] = 1
        print('队伍信息get成功')
    else:
        resJson['state'] = 0
        print('队伍信息get失败嗷嗷嗷')

    return  jsonify(resJson)



@app.route('/team_list', methods=['POST', 'GET'])
def team_list():
    '''
    get:'class_id'
    
    :return:
    class_info: {id: 69321, name: "面向对象程序设计", sup: 5, teams_count: 5},
    teams: [{ id: 1, count: 3, sup: 5, member: ["张一一", "张二二", "张三三"], info: "这里是简介这里是简介" },
    { id: 2, count: 3, sup: 5, member: ["李一一"], info: "这里是简介这里是简介这里是简介这里" },
    { id: 3, count: 3, sup: 5, member: [ "刘二二", "刘三三"], info: "这里介这里是简介这里是……" }
    ]
    '''
    print('>>>>in team list')
    data = to_Data()
    resJson = {}
    classInfo = {}
    classInfo['id'] = data['class_id']
    theClass = Class.query.filter_by(id = data['class_id']).one()
    classInfo['name'] = theClass.name
    classInfo['sup'] = theClass.limit
    classInfo['teams_count'] = Team.query.filter_by(class_id = data['class_id']).count()
    resJson['class_info'] = classInfo
    print('class info: ', classInfo)

    theTeam = Team.query.filter_by(class_id = data['class_id']).all()
    print('the team: ', theTeam)
    teamInfo = []
    for t in theTeam:
        info = {}
        info['id'] = t.id
        info['count'] = ClassHasStu.query.filter(ClassHasStu.class_id == data['class_id'],
                                        ClassHasStu.team_id == t.id).count()
        info['sup'] = theClass.limit
        members = []
        stus = ClassHasStu.query.filter(ClassHasStu.class_id == data['class_id'],
                                        ClassHasStu.team_id == t.id).all()
        for s in stus:
            stuName = Users.query.filter_by(openId = s.user_id).one()
            members.append(stuName.name)
        info['member'] = members
        teamInfo.append(info)

    resJson['teams'] = teamInfo
    print('team info: ', teamInfo)

    if teamInfo!=[] or classInfo!=[]:
        resJson['state'] = 1
        resJson['info'] = '队伍列表返回成功'
    else:
        resJson['state'] = 0
        resJson['info'] = '队伍列表返回失败。。'
    print(resJson)
    return jsonify(resJson)



@app.route('/team_create2', methods=['POST', 'GET'])
def team_create2():
    '''
    get:
    'leader_id': app.globalData.OPEN_ID,
    'team_info': e.detail.value.info,
    'team_invitors': this.data.invitors,
    'team_id': this.data.team.id,
    'team_sup': this.data.team.sup,
    'class_id': app.globalData.class_id,
    return: state, info
    '''
    print(">>>>>in  team create 2")
    data = to_Data()
    #更改team表中的
    newTeam = Team(id=data['team_id'], cap = data['team_sup'],
                   leader_id=data['leader_id'],class_id=data['class_id'],
                   full=0, msg=data['team_info'])
    newClassHasStu = ClassHasStu.query.filter(ClassHasStu.user_id==data['leader_id'],
                                              ClassHasStu.class_id==data['class_id']).one()
    newClassHasStu.team_id  =  data['team_id']
    db.session.add(newTeam)
    db.session.commit()
    print('新建的队伍：', newTeam)

    #更改invite request表中的
    #print(data['team_invitors'])
    invitors = []
    for n in data['team_invitors']:
        stu = Users.query.filter_by(name=n).all()
        for s in stu:
            stuId = ClassHasStu.query.filter(ClassHasStu.user_id==s.openId,
                                             ClassHasStu.class_id==data['class_id']).one()
            if stuId is not None:
                print('student find: ', stuId)
                invitors.append(stuId)
                continue
    flag = 0
    for s in invitors:
        newInvite=InviteRequest(team_id=data['team_id'], guest_id = s.user_id)
        db.session.add(newInvite)
        db.session.commit()
        flag = 1

    resJson = {}
    if newTeam is not None and flag == 1:
        resJson['state'] = 1
        resJson['info'] = '创建队伍成功！'
        print('队伍创建成功')
    else:
        resJson['state'] = 0
        resJson['info'] = '遇到了点问题嗷'
        print('遇到了点问题嗷')
    return jsonify(resJson)



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
    print(">>>>in team create 1")
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
    print('>>>>>in class list')
    data = to_Data()
    resJosn = {}
    classes = ClassHasStu.query.filter_by( user_id=data['open_id']).distinct().all()
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
        teams = Team.query.filter_by(class_id = c.class_id).count()
        print('team num: ', teams)
        classx['team_numbers'] = int(teams)
        res.append(classx)
        flag1 = 1
    resJosn['classes'] = res

    resUser = {}
    userName = Users.query.filter_by(openId = data['open_id']).all()
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
    notIn = ClassHasStu.query.filter (ClassHasStu.class_id==data['class_invite_id'] , ClassHasStu.user_id==data['stu_id']).all()
    print('class and stu: ',notIn)
    if theClass[0] is None :
        print('班级不存在')
        resJson['state'] = 0
        resJson['info'] = '邀请码输入错误，班级不存在嗷'
        return jsonify(resJson)
    if  notIn !=[] :
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
        newUser = Users(id=str(10000+ get_rand()), name = '新同学', openId=data['open_id'] , sno = '1000000')
        db.session.add(newUser)
        db.session.commit()
        print ('添加成功')
        resJson['student_id'] = None
        resJson['state'] = 0
    resJson['info'] = 'success'
    return jsonify(resJson)

# "http://127.0.0.1:5000/showJoinRequest"
@app.route('/showJoinRequest',methods=['POST','GET'])
def showJoinRequest():
    print( 'in showJoinRequest ....')
    data=to_Data()
    print(data['student_id'])#这是一个openid
    teamres=Team.query.filter_by(cap=data['student_id']).all()#找到以openid为student_id的学生为队长的队伍
    teamList = []
    for x in teamres:
        teamTmp = {}
        teamTmp['id']=x.id
        teamList.append(teamTmp)
    resJson = {}
    if teamList != []:#如果teamList不为空就在joinRequest表中查找加入该学生队伍的请求
        print('this student is a captain')
       # print(teamList[0]['id'])
        for i in range(0,len(teamList)):
            requestres=JoinRequest.query.filter_by(team_id=teamList[i]['id'],request_state = 2).all()#找到以该学生为队长的第i个队伍收到的申请
            returnList=[]
            for x in requestres:#对于队伍i收到的每条申请
                print(x.join_request_id)
                returnTmp={}
                returnTmp['id']=x.join_request_id
                getcap=Team.query.filter_by(id=x.team_id).all()#在队伍表中找到队伍的队长id
                print('classid',getcap[0].class_id)
                classsearch = Class.query.filter_by(id=getcap[0].class_id).all()  # 找到队伍所在的班级
                returnTmp['class_name'] = classsearch[0].name

                applicantsearch=Users.query.filter_by(openId=x.applicant_id)#申请人姓名
                returnTmp['applyer']=applicantsearch[0].name
                returnTmp['team_id']=x.team_id#队伍id

                member=[]
                membersearch=ClassHasStu.query.filter_by(team_id=x.team_id,class_id=classsearch[0].id).all()#在用户-队伍表中找到所有的对应关系
                for y in membersearch:#找到队伍中所有成员的名字
                    usersearch=Users.query.filter_by(openId=y.user_id).all()
                    member.append(usersearch[0].name)
                returnTmp['member']=member
                mesearch=Users.query.filter_by(openId=x.applicant_id).all()#找到申请人的名字
                returnTmp['me']=mesearch[0].name
            #returnTmp['read']=x.request_state
                returnTmp['read']=True
                returnTmp['time'] = '2019-05-20 13:17'
                returnList.append(returnTmp)

        if(returnList==[]):
            print('return list is null')
            newTmp={}
            newTmp['applyer']='开发者'
            newTmp['team_id']='000'
            newTmp['time']='2000-00-00 00:00'
            newTmp['class_name']='新班级'
            newTmp['me']='me'
            newTmp['id']=0
            returnList.append(newTmp)

        print(returnList)

        resJson={}
        resJson['apply_data']=returnList
        resJson['info']='success'
        resJson['state']=1

        print(resJson)
        return jsonify(resJson)
    else:#如果该学生只是一个普通成员
      #teamres = Team.query.filter_by(cap=data['student_id']).all()
      print('the student is amenmber')
      returnList=[]
      newTmp = {}
      newTmp['applyer'] = '开发者'
      newTmp['team_id'] = '000'
      newTmp['time'] = '2000-00-00 00:00'
      newTmp['class_name'] = '新班级'
      newTmp['me'] = 'me'
      newTmp['id'] = 0
      returnList.append(newTmp)
      resJson = {}
      resJson['apply_data'] = returnList
      resJson['info'] = 'success'
      resJson['state'] = 1

      print(resJson)
      return jsonify(resJson)

# "http://127.0.0.1:5000/inviteDetail"
@app.route('/applicationDetail',methods=['POST','GET'])
def applicationDetail():
    print( 'in applicationDetail ....')
    data = to_Data()
    print(data['apply_msg_id'])
    joinsearch = JoinRequest.query.filter_by(join_request_id=data['apply_msg_id']).all()  # 在表中找到这一条邀请
    joinsearch[0].request_read=1#标为已读
    db.session.commit()

    dataRes={}
    dataRes['id']=data['apply_msg_id']

    applicantsearch = Users.query.filter_by(openId=joinsearch[0].applicant_id).all()
    dataRes['applyer'] = applicantsearch[0].name

    getcap = Team.query.filter_by(id=joinsearch[0].team_id).all()  # 在队伍表中找到队伍的队长id
    # capsearch = Users.query.filter_by(id=getcap[0].id).all()   在用户表中找到队长的名字
    # dataRes['cap'] = capsearch[0].name

    classsearch = Class.query.filter_by(id=getcap[0].class_id).all()  # 找到队伍所在的班级
    dataRes['class_name'] = classsearch[0].name

    dataRes['team_id']=joinsearch[0].team_id
    member = []
    membersearch = ClassHasStu.query.filter_by(team_id=joinsearch[0].team_id,class_id=classsearch[0].id).all()  # 在用户-队伍表中找到所有的对应关系
    for x in membersearch:  # 找到队伍中所有成员的名字
        usersearch = Users.query.filter_by(openId=x.user_id).all()
        member.append(usersearch[0].name)
    dataRes['member'] = member

    dataRes['me'] = 'me'
    dataRes['time'] = '2019-05-20 13:16'
    dataRes['read']=True
    resJson={}
    resJson['invite_data']=dataRes
    resJson['state']=1
    resJson['info']='success'
    print(resJson)
    return jsonify(resJson)

# "http://127.0.0.1:5000/applicationHandle"
@app.route('/applicationHandle',methods=['POST','GET'])
def applicationHandle():
    print('in applicationHandle ....')
    data = to_Data()
    print(data['apply_msg_id'])

    resJson = {}
    resJson['info'] = 'success'

    if data['option'] == 0:  # 拒绝
        applysearch = JoinRequest.query.filter_by(join_request_id=data['apply_msg_id']).all()  # 在表中找到这一条邀请
        applysearch[0].request_state = 0  # 标为拒绝
        db.session.commit()
        resJson['state'] = 1
        return jsonify(resJson)
    elif data['option'] == 1:

        applysearch = JoinRequest.query.filter_by(join_request_id=data['apply_msg_id']).all()
        getteam = Team.query.filter_by(id=applysearch[0].team_id).all()  # 找到收到邀请的队伍
        teamuser = ClassHasStu.query.filter_by(class_id=getteam[0].class_id, user_id=applysearch[0].applicant_id).all()
        print('getteam[0].id', getteam[0].id)
        #print('getteam[0].class_id', getteam[0].class_id)
        #print('teamuser[0].team_id', teamuser[0].team_id)
        if teamuser[0].team_id is not '0':  # 如果该成员已经加入了别的队伍，那么操作失败，返回state为0
            print('error')
            print('teamuser[0].team_id', teamuser[0].team_id)
            resJson['state'] = 0
            return jsonify(resJson)
        applysearch[0].request_state = 1  # 标为接受
        db.session.commit()

        # getclass=Class.query.filter_by(id=getteam[0].class_id).all()#找到队伍的班级

        teamuser[0].team_id = getteam[0].id
        db.session.commit()

        resJson['state'] = 1
        return jsonify(resJson)
    elif data['option'] == 2:  # 忽略
        resJson['state'] = 1
        return jsonify(resJson)

# "http://127.0.0.1:5000/applicationDelete"
@app.route('/applicationDelete',methods=['POST','GET'])
def applicationDelete():
    print('in applicationDelete ....')
    data = to_Data()
    print(data['delete_msg_id_list'])
    flag=0
    if len(data['delete_msg_id_list'])==0:
        print('没有消息被选中')
    else:

        for i in range(0,len(data['delete_msg_id_list'])):
            flag=0
            joinfind=JoinRequest.query.filter_by(join_request_id=data['delete_msg_id_list'][i]).first()
            db.session.delete(joinfind)
            db.session.commit()
            print('删除成功')
            flag=1
    resJson={}
    resJson['state']=1
    if flag==1:
        resJson['info']='success'
    else:
        resJson['info']='fail'
    return jsonify(resJson)

# "http://127.0.0.1:5000/showInviteRequest"
@app.route('/showInviteRequest',methods=['POST','GET'])
def showInviteRequest():
    print( 'in showInviteRequest ....')
    data=to_Data()
    print(data['student_id'])
    inviteres=InviteRequest.query.filter_by(guest_id=data['student_id'],request_state = 2).all()
                                        #找到以id为student_id的学生收到的未处理的邀请
                                        #还需要添加条件
    inviteList = []
    for x in inviteres:
        inviteTmp = {}
        inviteTmp['invite_request_id']=x.invite_request_id
        inviteList.append(inviteTmp)

    resJson = {}
    returnList=[]
    print(inviteList)

    if inviteList != []:#如果inviteList不为空就查询请求的具体信息
        for x in inviteres:
            returnTmp={}
            returnTmp['id']=x.invite_request_id
            getcap=Team.query.filter_by(id=x.team_id).all()#在队伍表中找到队伍的队长id
            print('getcap',getcap[0].id)
            capsearch=Users.query.filter_by(openId=getcap[0].cap).all()#在用户表中找到队长的名字
            print('capsearch',capsearch[0].name)
            returnTmp['cap']=capsearch[0].name
            returnTmp['team_id']=x.team_id

            member=[]
            membersearch=ClassHasStu.query.filter_by(team_id=x.team_id).all()#在用户-队伍表中找到所有的对应关系
            print('membersearch',membersearch)
            for y in membersearch:#找到队伍中所有成员的名字
                usersearch=Users.query.filter_by(openId=y.user_id).all()
                member.append(usersearch[0].name)
            returnTmp['member'] = member

            returnTmp['me']='me'
            #returnTmp['read']=x.request_state
            if(x.request_state==0):
                returnTmp['read']=False
            else:
                returnTmp['read']=True
            returnTmp['time'] = '2019-05-20 13:17'#没有确定是使用时间戳还是字符串
            returnList.append(returnTmp)
        print(returnList)

        resJson={}
        resJson['invite_data']=returnList
        resJson['info']='success'
        resJson['state']=1

    else: #如果该学生没有收到邀请

        returnTmp={}
        returnTmp['cap']='开发者'
        returnTmp['team_id']='000'
        returnTmp['read']=True
        returnTmp['time'] = '2000-00-00 00:00'
        returnList.append(returnTmp)
        resJson['invite_data']=returnList
        resJson['info'] = 'success'
        resJson['state'] = 1

    print(resJson)
    return jsonify(resJson)

# "http://127.0.0.1:5000/inviteDetail"
@app.route('/inviteDetail',methods=['POST','GET'])
def inviteDetail():
    print( 'in inviteDetail ....')
    data = to_Data()
    print(data['invite_msg_id'])
    invitesearch = InviteRequest.query.filter_by(invite_request_id=data['invite_msg_id']).all()  # 在表中找到这一条邀请
    invitesearch[0].request_read=1#标为已读
    db.session.commit()

    dataRes={}
    dataRes['id']=data['invite_msg_id']

    getcap = Team.query.filter_by(id=invitesearch[0].team_id).all()  # 在队伍表中找到队伍的队长id
    capsearch = Users.query.filter_by(openId=getcap[0].id).all()  # 在用户表中找到队长的名字
    dataRes['cap'] = capsearch[0].name

    dataRes['team_id']=invitesearch[0].team_id
    member = []
    membersearch = ClassHasStu.query.filter_by(team_id=invitesearch[0].team_id).all()  # 在用户-队伍表中找到所有的对应关系
    for x in membersearch:  # 找到队伍中所有成员的名字
        usersearch = Users.query.filter_by(openId=x.user_id).all()
        member.append(usersearch[0].name)
    dataRes['member'] = member

    dataRes['me'] = 'me'
    dataRes['time'] = '2019-05-20 13:17'
    dataRes['read']=True
    resJson={}
    resJson['invite_data']=dataRes
    resJson['state']=1
    resJson['info']='success'
    print(resJson)
    return jsonify(resJson)

# "http://127.0.0.1:5000/inviteHandle"
@app.route('/inviteHandle',methods=['POST','GET'])
def inviteHandle():
    print( 'in inviteHandle ....')
    data = to_Data()
    print(data['invite_msg_id'])

    resJson={}
    resJson['info']='success'

    if data['option']==0:#拒绝
        invitesearch = InviteRequest.query.filter_by(invite_request_id=data['invite_msg_id']).all()  # 在表中找到这一条邀请
        invitesearch[0].request_state = 0  # 标为拒绝
        db.session.commit()
        resJson['state']=1
        return jsonify(resJson)
    elif data['option']==1:

        invitesearch=InviteRequest.query.filter_by(invite_request_id=data['invite_msg_id']).all()
        print('invitesearch',invitesearch[0].team_id)
        getteam = Team.query.filter_by(id=invitesearch[0].team_id).all()  # 找到发出邀请的队伍
        print('getteam',getteam[0].class_id)
        teamuser = ClassHasStu.query.filter_by(class_id=getteam[0].class_id, user_id=data['student_id']).all()
        print('teamuser',teamuser[0].team_id)
        if teamuser[0].team_id is not '0': # 如果该成员已经加入了别的队伍，那么操作失败，返回state为0
            resJson['state'] = 0
            return jsonify(resJson)

        invitesearch[0].request_state = 1  # 标为接受
        db.session.commit()

       # getclass = Class.query.filter_by(id=getteam[0].class_id).all()  # 找到队伍的班级

        teamuser[0].team_id=getteam[0].id
        db.session.commit()

        #还需要在表中删除掉邀请
        resJson['state']=1
        return jsonify(resJson)
    elif data['option']==2:#忽略
        resJson['state']=1
        return jsonify(resJson)


# "http://127.0.0.1:5000/inviteDelete"
@app.route('/inviteDelete',methods=['POST','GET'])
def inviteDelete():
    print('in inviteDelete ....')
    data = to_Data()
    print(data['delete_msg_id_list'])
    flag=0
    if len(data['delete_msg_id_list'])==0:
        print('没有消息被选中')
    else:

        for i in range(0,len(data['delete_msg_id_list'])):
            print(i)
            print(data['delete_msg_id_list'][i])
            flag=0
            invitefind=InviteRequest.query.filter_by(invite_request_id=data['delete_msg_id_list'][i]).first()
            db.session.delete(invitefind)
            db.session.commit()
            print('删除成功')
            flag=1
    resJson={}
    resJson['state']=1
    if flag==1:
        resJson['info']='success'
    else:
        resJson['info']='fail'
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

    print ( resJson)
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
        print (OK)
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