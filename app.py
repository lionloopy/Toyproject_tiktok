from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.fgag4po.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/playList')
def posting():
   return render_template('posting.html')

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

@app.route("/posting", methods=["GET"])
def posting_get():
    comment_list = list(db.comments.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})

# url = 'https://www.melon.com/landing/playList.htm?type=djc&plylstTypeCode=M20002&plylstSeq=453051002'
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)
#
# soup = BeautifulSoup(data.text, 'html.parser')

# frm > div > table > tbody > tr:nth-child(4) > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a
# frm > div > table > tbody > tr:nth-child(5) > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a

# musics = soup.select('div > table > tbody > tr')
# for music in musics:
#     a = music.select_one('td > div > div > div.ellipsis.rank01 > span > a')
#     if a is not None:
#         print(a.text)

# frm > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > a > img
# frm > div > table > tbody > tr:nth-child(4) > td:nth-child(3) > div > a > img
# images = soup.select('div > table > tbody > tr')
# for img in images:
#     b = img.select_one('td > div > a > img')
#     print(b['src'])

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
