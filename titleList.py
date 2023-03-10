from flask import Flask, render_template, request, jsonify
from werkzeug.debug import console

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