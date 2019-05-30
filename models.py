from exts import db

class Admin(db.Model):
    __tablename__ = 'admin'
    Adminaccount = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True)
    Password = db.Column(db.String(255, 'utf8_general_ci'), nullable=False)

class Project(db.Model):
    __tablename__ = 'project'
    ID = db.Column(db.Integer, primary_key=True)
    SNo = db.Column(db.ForeignKey('student.SNo', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    Project = db.Column(db.String(255))
    Award = db.Column(db.String(255))
    Code = db.Column(db.String(255))
    student = db.relationship('Student', primaryjoin='Project.SNo == Student.SNo', backref='projects')

class Student(db.Model):
    __tablename__ = 'student'
    SNo = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, index=True)
    Avatar = db.Column(db.String(255, 'utf8_general_ci'), index=True)
    SName = db.Column(db.String(255, 'utf8_general_ci'), nullable=False)
    Grade = db.Column(db.String(255, 'utf8_general_ci'), nullable=False)
    Group = db.Column(db.String(255, 'utf8_general_ci'), nullable=False)
    Telephone = db.Column(db.String(255, 'utf8_general_ci'))
    WeChat = db.Column(db.String(255, 'utf8_general_ci'))
    QQ = db.Column(db.String(255, 'utf8_general_ci'))
    MailBox = db.Column(db.String(255, 'utf8_general_ci'))
    Other = db.Column(db.String(255, 'utf8_general_ci'))
    Occupation = db.Column(db.String(255, 'utf8_general_ci'))
    WorkAddress = db.Column(db.String(255, 'utf8_general_ci'))
    Direction = db.Column(db.String(255, 'utf8_general_ci'))

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, index=True)
    name = db.Column(db.String(255, 'utf8_general_ci'),nullable=False)
    openId = db.Column(db.String(255, 'utf8_general_ci'),nullable=False)
    sno = db.Column(db.String(255, 'utf8_general_ci'),nullable=False)
class Class(db.Model):
    '''
    id（可做邀请码）
    名称
    队伍人数上限
    管理密码
    '''
    __tablename__ = 'class'
    id = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, index=True)
    name = db.Column(db.String(255, 'utf8_general_ci'),nullable=False)
    limit = db.Column(db.Integer)
    pwd = db.Column(db.String(255, 'utf8_general_ci'),nullable=False)

class Team(db.Model):
    '''
    id
    队长id
    队伍已有人数
    班级_id
    队伍满员标记
    信息 /255
    '''
    __tablename__ = 'team'
    id = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, index=True)
    cap = db.Column(db.String(255, 'utf8_general_ci'), db.ForeignKey('users.id'))
    # user_id = db.Column(db.String(255, 'utf8_general_ci'), db.ForeignKey('users.id'))
    class_id = db.Column(db.String(255, 'utf8_general_ci'), db.ForeignKey('class.id'))
    full = db.Column(db.Integer)
    msg =  db.Column(db.String(255, 'utf8_general_ci'))

class TeamHasStu(db.Model):
    '''
      班级id
      队伍id
      学生id
    '''
    __tablename__='team_has_stu'
    id = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, index=True)
    class_id=db.Column(db.String(255,'utf8_general_ci'),db.ForeignKey('class.id'))
    team_id=db.Column(db.String(255,'utf8_general_ci'),db.ForeignKey('team.id'))
    user_id=db.Column(db.String(255,'utf8_general_ci'),db.ForeignKey('users.id'))

class ClassHasStu(db.Model):
    '''
    id
    班级id
    学生id
    队伍id
    '''
    __tablename__ = 'class_has_stu'
    id = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True, index=True)
    class_id = db.Column(db.String(255, 'utf8_general_ci'), db.ForeignKey('class.id'))
    user_id = db.Column(db.String(255, 'utf8_general_ci'), db.ForeignKey('users.id'))
    team_id = db.Column(db.String(255, 'utf8_general_ci'), db.ForeignKey('team.id'))

class JoinRequest(db.Model):
    ''''
     message id
     申请者id
     申请加入的队伍id
     是否已读（对队长而言）
     请求状况（是否通过）
    '''
    __tablename__='join_request'
    join_request_id=db.Column(db.String(255,'utf8_general_ci'),primary_key=True)
    applicant_id=db.Column(db.String(255,'utf8_general_ci'),db.ForeignKey('users.id'))
    team_id=db.Column(db.String(255,'utf8_general_ci'),db.ForeignKey('team.id'))
    request_read =db.Column(db.Integer,default=0)#0为未读
    request_state = db.Column(db.Integer,default=0)

class InviteRequest(db.Model):
    '''
      message id
      邀请队伍id
      被邀请者id
      请求状况（是否通过）
    '''
    _tablename__ = 'invite_request'
    invite_request_id = db.Column(db.String(255, 'utf8_general_ci'), primary_key=True)
    team_id = db.Column(db.String(255,'utf8_general_ci'), db.ForeignKey('team.id'))
    guest_id = db.Column(db.String(255,'utf8_general_ci'), db.ForeignKey('users.id'))
    request_state = db.Column(db.Integer, default=0)
