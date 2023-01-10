from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

# db 연결 시 certifi 사용함(없으면 db연결이 저는 안됨)
ca = certifi.where()

client = MongoClient('mongodb+srv://yunseo:sparta@cluster0.6bemlvq.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('signup_index.html')

@app.route("/api/signup", methods=["POST"])
def web_signup_post():
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    doc = {
        'username':name_receive,
        'email':email_receive,
        'password':password_receive
    }
    db.users.insert_one(doc)

    return jsonify({'msg': '가입 완료'})

@app.route("/signin", methods=["GET"])
def web_signup_get():
    user_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'users': user_list})

# 5100 포트로 했음
if __name__ == '__main__':
    app.run('0.0.0.0', port=5100, debug=True)