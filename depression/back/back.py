from flask import Flask,request,session
import json
from flask_cors import CORS
from config import UPDATE_PATH_AUDIO, UPDATE_PATH_VIDEO
from extract_audio import extract_Audio,audio_capture
import os
# from flask_login import LoginManager, UserMixin,login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import datetime
from video_capture import video_capture
from audio import audio_Feature,Feature,audio_Model
from face import video_feature,HDR,video_Model

app = Flask(__name__) #创建Flask类的实例，第一个参数是模块或者包的名称

app.config['SQLALCHEMY_DATABASE_URI']=r'sqlite:///E:\myworkspace\depression\depression\back\db\db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True


app.config['JSON_AS_ASCII']=False # 支持中文显示
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

openface_out_dir = 'E:/myworkspace/depression/depression/back/video/processed/'

class User( db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=True)
    # historys = db.relationship("History",backref = 'user')

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    

class History(db.Model):
    __tablename__ = 'history'
    hid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # uid = db.Column(db.Integer,nullable=False)
    time = db.Column(db.String(200),nullable=False)
    score = db.Column(db.Integer,nullable=False)
    uid = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    # u = db.relationship('User', back_populates='historys')

    def __init__(self,uid,time,score):
        self.uid = uid
        self.time = time
        self.score = score


@app.route('/login', methods=['POST','GET'])
def login_post():
    username = request.form.get("username")
    print(username)
    password = request.form.get("password")
    print("password"+password)
    if username == "" or password == "":
        print('用户名和密码不能为空！！！')
        data = {'code': 401, 'data': '', 'msg': 'username or password can not null'}
        return json.dumps(data)
    user = User.query.filter_by(username=username).first()
    
    if user is None or not user.check_password(password):
        print('用户名或密码错误！！！')
        data = {'code': 401, 'data': '', 'msg': 'username or password is wrong'}
        return json.dumps(data)
    session['user_id'] = user.id
    print('login success')
    data = {'code': 200, 'data': user.id, 'msg': 'login success'}
    return json.dumps(data)

@app.route('/register', methods=['POST','GET'])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    repassword = request.form.get("repassword")
    email = request.form.get("email")
    
    if username == "" or password == "":
        print('用户名和密码不能为空！！！')
        data = {'code': 401, 'data': '', 'msg': 'username or password can not null'}
        return json.dumps(data)
    if password != repassword:
        print('两次密码不一致！！！')
        data = {'code': 401, 'data': '', 'msg': 'password is not equal to repassword'}
        return json.dumps(data)
    user = User.query.filter_by(username=username).first()
    if user is not None:
        print('用户名重复！！！')
        data = {'code': 401, 'data': '', 'msg': 'user is existe'}
        return json.dumps(data)
    user = User(username=username,password=password,email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    data = {'code': 200, 'data': '', 'msg': 'register success'}
    return json.dumps(data)

@app.route('/history',methods=['POST','GET'])
def history():

    user_id = session['user_id']
    historys = History.query.filter(History.uid==user_id).all()

    if historys is None:
        data = {'code': 401, 'data': '', 'msg': 'historys is not existe'}
        return json.dumps(data)
    else:
        print('----------------------')
        print(type(historys))
        y=[]
        z=[]
        x=dict()
        j=0
        for i in historys:
            y.append(str(i.time))
            z.append(str(i.score))
        x['score']=z
        x['time']=y
        data = {'code': 200, 'data':x ,'msg': 'historys success'}
        return json.dumps(data)
    


@app.route('/Score', methods=['POST','GET']) # 使用methods参数处理不同HTTP方法
def GetScore():
      score = request.args.get('Score')
      session['score'] = score
      data = {'code': 200, 'data':'', 'msg': 'Score success'}
      return json.dumps(data)

@app.route('/video', methods=['POST','GET'])
def GetVideo():
      data = request.files
      print(f"video request files: {data}")
      file = data['file']
      print(f"video request file: {file}")
      Time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
      name = Time
      video_path = UPDATE_PATH_VIDEO+name+'_'+'video.mp4'
      print(f"GetVideo: {video_path}")
      file.save(video_path)
    #   video_feature_path = UPDATE_PATH_VIDEO+name+'_'+'video_capture.mp4'


      #面部
      print("现在正在获得面部初始文件...")
      video_feature(video_path)
      print("获得面部初始文件结束...")
      video_new_path = openface_out_dir +name+'_'+'video.csv'
      HDR_path = UPDATE_PATH_VIDEO + name+'_'+'video_capture.csv'
      print("现在正在获得面部HDR文件...")
      HDR(video_new_path,HDR_path)
      print("获得面部HDR文件结束...")
      print("现在正在视频频模型...")
      videoScore = video_Model(HDR_path)
      print(f"视频频模型结束... videoScore: {videoScore}")
      # 转换为百分制
      centesimal_video_score = videoScore/24 * 100

      data = {'code': 200, 'data':int(centesimal_video_score), 'msg': 'Video success'}
      return json.dumps(data)

@app.route('/Time', methods=['POST','GET']) # 使用methods参数处理不同HTTP方法
def GetTime():

    timeBegin = request.args.get('timeBegin')
    session['st'] = int(int(timeBegin)/1000)
    print(timeBegin)
    timeEnd = request.args.get('timeEnd')
    session['et'] = int(int(timeEnd)/1000)
    print(timeEnd)
    data = {'code': 200, 'data':'', 'msg': 'Time success'}
    return json.dumps(data)


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    if os.path.exists('db/db.db'):
        pass
    else:
        db.create_all()
    app.run(host='0.0.0.0')
    