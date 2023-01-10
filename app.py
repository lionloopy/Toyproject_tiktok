from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.mih9efs.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('titleList.html')

@app.route("/music", methods=["POST"])
def music_post():
    music_receive = request.form['music_give']
    music_list = list(db.musics.find({}, {'_id': False}))
    count = len(music_list)+1

    doc = {
        'heart':count,
        'music':music_receive,
        'count':0
    }

    db.musics.insert_one(doc)

    return jsonify({'msg':'순위 정리 완료!'})


@app.route("/musics", methods=["GET"])
def music_get():
    music_list = list(db.musics.find({},{'_id':False}))
    return jsonify({'musics':music_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)