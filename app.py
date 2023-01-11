from bson import ObjectId
import jwt
import datetime
import hashlib
import requests

from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

from pymongo import MongoClient
import certifi

from bs4 import BeautifulSoup

##### 회원가입
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.fgag4po.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/signup')
def sign_up():
    return render_template('signup_index.html')

@app.route("/api/signup", methods=["POST"])
def web_signup_post():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        'name': name_receive,
        'email': email_receive,
        'password': password_hash
    }
    db.users.insert_one(doc)

    return jsonify({'msg': '가입 완료'})

@app.route("/signin", methods=["GET"])
def web_signup_get():
    user_list = list(db.signup.find({}, {'_id': False}))
    return jsonify({'users': user_list})

##### 로그인
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

@app.route("/api/sign_in", methods=["POST"])
def sign_in():
    email_receive = request.form['email_give']
    password_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'email': email_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': email_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECERY_KEY, algorithm='HS256')
        return jsonify({'result': 'success','token': token, 'msg': '로그인 성공!'})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})

#### 메인페이지
@app.route('/page/main')
def main():
    return render_template('main_posting.html')

@app.route("/music", methods=["POST"])
def music_post():
    url_receive = request.form['url_give']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.melon.com/landing/playList.htm?type=djc&plylstTypeCode=M20002&plylstSeq=453051002', headers=headers)

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

#### 상세페이지
@app.route('/page/detail')
def posting():
   return render_template('posting.html')

@app.route("/posting", methods=["GET"])
def posting_get():
    music_list = list(db.musics.find({}, {'_id': False}))
    # comment_list = list(db.comments.find({}, {'_id': False}))
    return jsonify({'musics': music_list})

# @app.route("/posting_detail", methods=["GET"])
# def posting_detail_get():
#
#     rank =
#     music = db.musics.find_one({'rank': rank})
#
#     # comment_list = list(db.comments.find({}, {'_id': False}))
#
#     return jsonify({'musics': music_list})


@app.route("/posting", methods=["POST"])
def comment_post():
    # name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    comment_list = list(db.comments.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'num': count,
        'comment': comment_receive
    }
    db.comments.insert_one(doc)

    return jsonify({'msg': '저장되었습니다!'})

@app.route("/posting/delete", methods=["POST"])
def comment_delete():

    number_receive = request.form['number_give']
    comments_receive = request.form['comments_give']

    doc = {
        'num' : number_receive,
        'comment' : comments_receive
    }

    db.comments.delete_one(doc)

    return jsonify({'msg': '삭제되었습니다!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
