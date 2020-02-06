from flask import Flask,request,jsonify
import os,time
from datetime import timedelta
from app.models import app

# app = Flask(__name__)

app.debug = True








#盐加密
#

app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(7)#更改session过期时间


from .home import home as home_bluePrint
from .admin import admin as admin_bluePrint

app.register_blueprint(home_bluePrint)
app.register_blueprint(admin_bluePrint,url_prefix="/admin")



@app.route('/upload',methods=['POST'])
def upload():

    if request.files.get('file'):
        dir = os.path.abspath('.')
        path = '{}/{}/{}'.format(dir,'app','uploads')
        file = request.files.get('file')
        print(file.filename)
        name = file.filename
        filetype = name.split('.')[-1]
        if filetype in ['png','gif','jpg','jpeg']:
            file.save('{}/{}'.format(path, file.filename))
            return jsonify({'status':'ok','img':file.filename})
        else:
            return jsonify({'status': 'false', 'img': file.filename})
    else:
        return jsonify({'status': 'false'})

