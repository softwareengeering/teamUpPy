from flask import Flask, render_template, request, make_response, send_file ,jsonify
from models import Admin, Student, Project, Users , Team , Class , ClassHasStu,InviteRequest,JoinRequest,TeamHasStu
from exts import db
import config, os
from methods import get_rand, get_Info, to_Data, to_List, to_Json, new_avatar_name, create_xlsx
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials = True) # 解决跨域问题

app.config.from_object(config)
db.init_app(app)
#fjdfjskd
url = "http://127.0.0.1:5000/"
@app.before_first_request
def init_db():
    print ('>>>>>>>>creating DB...')
    db.create_all()

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


# "http://127.0.0.1:5000/showJoinRequest"
@app.route('/showJoinRequest',methods=['POST','GET'])
def showJoinRequest():
    print( 'in showJoinRequest ....')
    data=to_Data()
    print(data['student_id'])
    teamres=Team.query.filter_by(cap=data['student_id']).all()#找到以id为student_id的学生为队长的队伍
    teamList = []
    for x in teamres:
        teamTmp = {}
        teamTmp['id']=x.id
        teamList.append(teamTmp)
    resJson = {}
    if teamList != []:#如果teamList不为空就在joinRequest表中查找加入该队伍的请求
        print('this student is a captain')
        print(teamList[0]['id'])
        requestres=JoinRequest.query.filter_by(team_id=teamList[0]['id']).all()
        # requestList=[]
        # for x in requestres:
        #     requestTmp={}
        #     requestTmp['join_request_id']=x.join_request_id
        #     requestTmp['applicant_id']=x.applicant_id
        #     requestTmp['team_id']=x.team_id
        #     requestTmp['request_state']=x.request_state
        #     requestList.append(requestTmp)       #还需要（队长的名字）、当前队伍成员、申请者姓名
        # print(requestList)

        returnList=[]
        for x in requestres:
            returnTmp={}
            returnTmp['id']=x.join_request_id
            getcap=Team.query.filter_by(id=x.team_id).all()#在队伍表中找到队伍的队长id
            capsearch=Users.query.filter_by(id=getcap[0].id).all()#在用户表中找到队长的名字
            returnTmp['cap']=capsearch[0].name
            returnTmp['team_id']=x.team_id

            member=[]
            membersearch=TeamHasStu.query.filter_by(team_id=x.team_id).all()#在用户-队伍表中找到所有的对应关系
            for y in membersearch:#找到队伍中所有成员的名字
                usersearch=Users.query.filter_by(id=y.user_id).all()
                member.append(usersearch[0].name)
            returnTmp['memeber']=member

            mesearch=Users.query.filter_by(id=x.applicant_id).all()
            returnTmp['me']=mesearch[0].name
            returnTmp['read']=x.request_state
            returnList.append(returnTmp)
        print(returnList)

        resJson={}
        resJson['apply_data']=returnList
        resJson['info']='success'
        resJson['state']=1
        print(resJson)
        return jsonify(resJson)
    else:#如果该学生只是一个普通成员
      #teamres = Team.query.filter_by(cap=data['student_id']).all()
      print('find nothing')
      return ("1")

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
        userTmp['student_info'] = {'':  , '':  }
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