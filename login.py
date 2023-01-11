import jwt, datetime, hashlib, certifi

from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)

from pymongo import MongoClient
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

client = MongoClient('mongodb+srv://yunseo:sparta@cluster0.6bemlvq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

##### 로그인
SECRET_KEY = 'SPARTA'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload['id']})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 존재하지 않습니다.'))


@app.route('/login')
def login():
    msg = request.args.get('msg')
    return render_template('index.html', msg=msg)


# 로그인 기능
# id,pw를 클라이언트에게 받아와 pw를 해쉬인코딩 하여 암호화한다.
# id와 암호화한 pw를 mongoDB에 있는지 확인하고, 없을시에는 result = None
# 클라이언트에게 받은 id와 pw가 mongoDB와 일치할 시 token을 생성한다.
# 클라이언트에게 토큰을 전송한다.
@app.route("/api/sign_in", methods=["POST"])
def sign_in():
    email_receive = request.form['email_give']
    password_receive = request.form['pw_give']
    # pw를 암호화합니다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 해당 유저를 찾습니다.
    result = db.users.find_one({'email': email_receive, 'password': pw_hash})
    # 찾으면 토큰을 만들어 발급합니다.
    if result is not None:
        payload = {'id': email_receive, 'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token, 'msg': '로그인 성공!'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})


##### 회원가입
ca = certifi.where()

client = MongoClient('mongodb+srv://yunseo:sparta@cluster0.6bemlvq.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta


@app.route('/signup')
def sign_up():
    return render_template('signup_index.html')


@app.route('/page/main')
def page_main():
    return render_template('titleList.html')


@app.route("/api/signup", methods=["POST"])
def web_signup_post():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {'name': name_receive, 'email': email_receive, 'password': pw_hash}
    db.users.insert_one(doc)

    return jsonify({'msg': '가입 완료'})


@app.route("/signin", methods=["GET"])
def web_signup_get():
    user_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'users': user_list})


@app.route('/playList')
def posting():
    return render_template('posting.html')


@app.route("/posting", methods=["POST"])
def comment_post():
    # name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    comment_list = list(db.comments.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {'num': count, 'comment': comment_receive}
    db.comments.insert_one(doc)

    return jsonify({'msg': '저장되었습니다!'})


@app.route("/posting", methods=["GET"])
def posting_get():
    comment_list = list(db.comments.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


@app.route("/music", methods=["POST"])
def music_post():
    url_receive = request.form['url_give']


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.melon.com/landing/playList.htm?type=djc&plylstTypeCode=M20002&plylstSeq=453051002',
                    headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

images = soup.select_one('div > table > tbody > tr')

a = soup.select('#frm > div > table > tbody > tr')

for music in a:
    for img in images:
         b = music.select_one('div > a > img')
    rank = music.select_one('div > span.rank').text[0:2].strip()
    title = music.select_one('div > div > div.ellipsis.rank01 > span > a').text.strip()
    singer = music.select_one('div > div > div.ellipsis.rank02 > a').text
    album = music.select_one('td:nth-child(6) > div > div > div > a').text
    if music is not None:
        doc = {
            'image': b['src'],
            'rank': rank,
            'title': title,
            'singer': singer,
            'album': album
        }
        db.musics.insert_one(doc)


@app.route("/music", methods=["GET"])
def music_get():
    music_list = list(db.musics.find({}, {'_id': False}))
    return jsonify({'musics': music_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)