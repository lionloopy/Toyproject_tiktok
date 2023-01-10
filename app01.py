import jwt
import datetime
import hashlib

from flask import Flask, render_template, request, jsonify, url_for, redirect
app = Flask(__name__)

from datetime import datetime, timedelta

from pymongo import MongoClient
client = MongoClient('mongodb+srv://yunseo:sparta@cluster0.6bemlvq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

SECERY_KEY = 'SPARTA'
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECERY_KEY, algorithms=['HS256'])
        id = payload['id']
        return render_template('index.html', username=id)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login',msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login',msg='로그인 정보가 존재하지 않습니다.'))

@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('index.html', msg=msg)
@app.route("/sign_in", methods=["POST"])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username':username_receive,'password':pw_hash})

    if result is not None:
        payload = {
            'id':username_receive,
            'exp': datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECERY_KEY, algorithm='HS256')
        return jsonify({'result':'success','token':token, 'msg':'로그인 성공!'})
    else:
        return jsonify({'result': 'fail','msg':'아이디/비밀번호가 일치하지 않습니다.'})

