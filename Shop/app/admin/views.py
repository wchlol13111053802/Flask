from . import admin
from flask import render_template,request,redirect
from ..models import User,UserLog,Goods,Sale,admin_log,Admin,Admin_opreate_log,db
import json

Session = db.session()

# 数据库关闭函数
def clo(Session):
    Session.commit()
    # 关闭session
    Session.close()

@admin.route('/') #登录界面
def index():
    return render_template('admin/index.html')


@admin.route('/index/',methods=['POST']) #登录验证账号
def login():
    print(request.form)
    return {'status':'ok'}

@admin.route('/out/') #退出登录
def out():
    return redirect('/admin/')

@admin.route('/goods/',methods=['POST'])
def add():
    result = ''.join(request.form.to_dict().keys())
    result = json.loads(result)
    print('键值',result)
    print('class',result['class'])
    goods = Goods(goods_class=result['class'],img='/path/1.jpg',name=result['name'],price=result['price'],number=result['number'])
    db.session.add(goods)
    db.session.commit()
    print('添加完毕')
    return 'success'

@admin.route('/goods/dele',methods=['POST'])
def dele():
    result = ''.join(request.form)
    result = json.loads(result)
    goods = Goods.query.filter_by(id=result['id']).first()
    db.session.delete(goods)
    db.session.commit()
    print(result)
    print('删除完毕')
    return 'success'
@admin.route('/goods/update',methods=['POST'])
def update():
    result = ''.join(request.form)
    result = json.loads(result)
    goods = Goods.query.filter_by(id=result['id']).first()
    goods.name = 'dong'
    db.session.delete(goods)
    db.session.commit()



@admin.route('/index/first/',methods=['POST','GET']) #请求的首页
def first():
    goods  = Goods.query.all()
    print(goods)
    return render_template('admin/first.html',con=goods,user=User.query.all(),data=[{'user':'宏小圣','order':'322','success':'120','pay':'423','relpay':'325','num':13},])