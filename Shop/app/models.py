# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer, String, DateTime,Text,Float,Boolean
from sqlalchemy import ForeignKey
import datetime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@127.0.0.1:3306/shop?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# db.Model = declarative_base()
# 
# 
# engine = create_engine('mysql+pymysql://root:toor@0.0.0.1:3306/shop?charset=utf8')
# 


# 每次执行数据库操作的时候，都需要创建一个session,相当于管理器(相当于Django的ORM的objects)
# Session = sessionmaker(bind=engine)
# 线程安全，基于本地线程实现每个线程用同一个session
# Session = scoped_session(Session)



#用户数据模型
class User(db.Model):
    __tablename__='user'
    __table_args__ = {'extend_existing': True}
    id =  db.Column(db.Integer,primary_key=True) #编号
    name =  db.Column(db.String(100),unique=True) #昵称
    pwd =  db.Column( db.String(100)) #密码
    email =  db.Column( db.String(100),unique=True) #邮箱
    phone =  db.Column( db.String(11),unique=True) #手机
    face =  db.Column( db.String(255),unique=True) #头像
    addTime =  db.Column( db.DateTime,index=True,default=datetime.datetime.utcnow()) #用户注册时间
    uuid =  db.Column( db.String(255),unique=True) #唯一标志符
    def __repr__(self):
        return "<User %r>"% self.name
#
# #用户查询
# def user():
#     result = User.query.all()
#     return result


#用户登录日志
class UserLog(db.Model):
    __tablename__='userlog'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer,primary_key=True) #编号
    user_id= db.Column( db.Integer,ForeignKey('user.id')) #所属会员
    ip =  db.Column( db.String(100)) #登录ip
    addtime =  db.Column( db.DateTime,index=True,default=datetime.datetime.utcnow()) #登录时间

    def __repr__(self):
        return "<Userlog %r>"%self.id


#购物车栏
class ShopCar(db.Model):
    __tablename__ = 'shopcar'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer,primary_key=True)
    name =  db.Column( db.String(100),unique=True) #购物车内商品名字
    status =  db.Column( db.Boolean) #商品是否付款
    icon =  db.Column( db.String(100)) #商品缩略图
    addTime =  db.Column( db.DateTime,index=True,default=datetime.datetime.utcnow()) #添加时间
    price =  db.Column( db.Float) #单个商品价钱
    number =  db.Column( db.Integer) #商品数量
    goods_id =  db.Column( db.Integer,  ForeignKey('goods.id')) #商品id
    def __repr__(self):
        return "<UserShopCar %r>"%self.name


#账单栏
class PriceOrder(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer, primary_key=True)
    name =  db.Column( db.String(100), unique=True)
    addTime =  db.Column( db.DateTime, index=True, default=datetime.datetime.utcnow())
    price =  db.Column( db.Float)
    number =  db.Column( db.Integer)

    def __repr__(self):
        return "<UserOrder %r>" % self.name

#商品
class Goods(db.Model):
    __tablename__ = 'goods'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer, primary_key=True)
    goods_class =  db.Column( db.String(100)) #商品分类
    img =  db.Column( db.String(120)) #商品图片
    name =  db.Column( db.String(100),unique=True) #商品名字
    price =  db.Column( db.Float) #价格
    number =  db.Column( db.Integer) #库存
    addTime =  db.Column( db.DateTime, index=True, default=datetime.datetime.utcnow())#入库时间
    def __repr__(self):
        return "<Goods %r>" % self.name



#---------------admin-------------------#

#销量
class Sale(db.Model):
    __tablename__ = 'Sale'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer, primary_key=True)
    good_id =  db.Column( db.Integer,ForeignKey('goods.id'))  # 商品id
    sale =  db.Column( db.Integer)  # 销量
    goods_class =  db.Column( db.Integer) #商品分类
    def __repr__(self):
        return "<Sale %r>" % self.sale


#管理员登录日志
class admin_log(db.Model):
    __tablename__ = 'adminlog'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer,primary_key=True)
    admin_id =  db.Column(db.String(10))
    ip =  db.Column(db.String(20))
    reason =  db.Column( db.Text) #登录原因
    addtime =  db.Column( db.DateTime,default=datetime.datetime.utcnow())

    def __repr__(self):
        return "<admin_log %r>" % self.reason


#管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}
    id =  db.Column( db.Integer, primary_key=True)  # 编号
    name =  db.Column( db.String(100), unique=True)  # 昵称
    pwd =  db.Column( db.String(100))  # 密码
    email =  db.Column( db.String(100), unique=True)  # 邮箱
    is_super =  db.Column(db.Integer) #是否为超级管理员
    def __repr__(self):
        return "<Admin %r>" % self.name


#操作日志
class Admin_opreate_log(db.Model):
    __tablename__ = 'oplog'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) #编号
    admin_id = db.Column(db.String(10)) #所属管理员
    ip = db.Column(db.String(20)) #登录ip
    operate = db.Column(db.Text) #操作记录
    addtime = db.Column(db.DateTime,index=True,default=datetime.datetime.utcnow()) #登陆时间


#提交创建表命令
# db.create_all()


