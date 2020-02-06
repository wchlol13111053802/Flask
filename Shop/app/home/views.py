from . import home
from flask import url_for,redirect,render_template,session,request,Request,jsonify
import os,base64,time,datetime
import random
from app.models import User,db,ShopCar
import json

Session = db.session()

from socket import *



# from blinker import Namespace
# from flask import request
#Namespace:命名空间

#定义信号
# dianshang = Namespace()
# fire_signal = dianshang.signal('fire')

#监听型号
# def fire_bullet(sender):
#     print(sender)
#     print('start fire bullet')
# fire_signal.connect(fire_bullet)

#发送一个信号
# fire_signal.send()

#定义一个登录信号，用户登录进来后
#发送一个登录信号，就能监听这个信号
#在监听这个信号以后，就记录当前这个用户登录的信息
#用信号的方式，记录用户的登录信息





#base64图片传递函数
def Img():
    file_list = ['']
    file_list.clear()
    img_list = os.listdir('app/static/img/NewT')
    for i in img_list:
        with open('app/static/img/NewT/' + i, 'rb') as f:
            img_stream = f.read()
            img_stream = base64.b64encode(img_stream)
            result = str(img_stream).replace("b'", '').replace("'", '')
            print(i)

            file_list.append(result)
    reverse = file_list.sort(reverse=True)
    print('倒叙',reverse)
    return file_list


@home.route('/back',methods=['POST','GET'])
def back():
    host = '192.168.3.6'  # 服务器的ip
    port = 12345  # 接口选择大于10000
    bufsize = 1024  # 定义缓冲
    addr = (host, port)
    udpClient = socket(AF_INET, SOCK_DGRAM)  # 创建socket客户端
    while True:
        data, addr = udpClient.recvfrom(bufsize)  # 成功发送至服务器端后，接收服务器发送的返回数据和返回地址
        print(data.decode(encoding='utf-8'), 'from', addr)
        return data.decode(encoding='utf-8')


@home.route('/chat',methods=['POST','GET'])
def chat():
    host = '192.168.3.6'  # 服务器的ip
    port = 12345  # 接口选择大于10000
    bufsize = 1024  # 定义缓冲
    data = ''.join(request.form)
    print('聊天室信息',''.join(request.form))
    addr = (host, port)
    udpClient = socket(AF_INET, SOCK_DGRAM)  # 创建socket客户端

    while True:
        if not data:
            break
        # data = data.encode(encoding="utf-8")
        udpClient.sendto(data.encode(encoding="utf-8"), addr)  # 发送数据

    return 'success'


@home.route('/',methods=['POST','GET'])
def index():
    file_list = ['']
    img_list = os.listdir('app/static/img/NewT')
    file_list.clear()
    decress_list = ['']
    decress_list.clear()


    print('浏览器地址',request.url)
    if '?' in request.url: #登录后跳转更换头像
        url_list = request.url.split('/')
        name = url_list[3][6:]
        # img = Session.query(User).filter_by(name=name).first().face
        img = User.query.filter_by(name=name).first().face
        type = img.split('.')[-1]
        with open('app/uploads/' + img, 'rb') as f:
            img_stream = f.read()
            img_stream = base64.b64encode(img_stream)
            result = str(img_stream).replace("b'", '').replace("'", '')
            print(img)
        print(name)
        return render_template('home/index.html', data={'file': [Img()],'icon':result,'type':type})

    else:
        session['username'] = 'wch' #未登录的首页
        session.permanent = True


        print(session)


        return render_template('home/index.html',data={'file':[Img()]})



#登录跳转路由
@home.route('/login/',methods=["GET"])
def login():
    data = request.json
    print(data)
    return render_template('home/login.html')

#登录输入路由444441
@home.route('/api/login',methods=["POST"])
def login_api():
    result = request.get_json()
    name = result['name']
    password = result['password']
    # try:
        # pwd = Session.query(User).filter_by(name=name).first().pwd
    pwd = User.query.filter_by(name=name).first().pwd

    print('查出来的密码',pwd)
    db.session.commit()
    if password==pwd:
        return '登陆成功'
    else:
        return '密码错误或账号错误'
    # except:
    #     print('数据库报错了')
    #     db.session.commit()
    #     print(result)
    #     return '登陆失败'

    # print(result)
    # return '登陆成功'

# 找回密码
@home.route('/find_password/')
def find_password():

    print('找回密码')
    return render_template('home/find_password.html')

#注册跳转路由
@home.route('/register/')
def register():
    return render_template('home/register.html')

#注册输入路由
@home.route('/api/register/',methods=["POST"])
def register_api():
    result = request.json
    print('前台数据json格式', result.values())
    if '' in result.values():
        print('本次没有全部填写完')
        print('注册表单里的内容', request.data)
        # img = result.get('img','没有图片')
        # print(img)
        # # if '没有图片' not in result['img']:
        # try:
        #     dir = os.path.abspath('.')
        #     path = '{}\{}\{}\{}'.format(dir, 'app', 'uploads',result['img'])
        #     os.remove(path)
        #     print('系统头像路径',path)
        # except:
        #     print('图片未找到')
        return '注册失败'
    else:
        print('本次全部填写完')
        print(type(result['email']))
        new_user = User(name=result['name'],pwd=result['password'],email=str(result['email']),phone=result['phone'],face=result['img'],addTime=datetime.datetime.utcnow(),uuid=str(time.localtime())+time.ctime())
        print(new_user)
        try:
            db.session.add(new_user)
            db.session.commit()
            # print('session里面的方法', db.session)
            # print('注册表单里的内容', request.data)
            return '注册成功'
        except:
            return '已经注册过了'


#用户点击请求路径
@home.route('/path/',methods=['POST','GET'])
def path_ro():
    result = request.get_json()
    print('用户点击事件',request.get_json())
    db.session.add(ShopCar(name=result['name'],price=result['price'],status=False,icon='/path/ic.jpg',number=1,goods_id=1))
    db.session.commit()
    return 'ok'

#购物车跳转路由
@home.route('/shop_car/',methods=['POST','GET'])
def shop_car():
    return render_template('home/shop_car.html')


@home.route('/pay/',methods=["POST"])
def pay():

    return jsonify({'statue':'ok'})

@home.route('/get/')
def get():
    return session.get('username')

