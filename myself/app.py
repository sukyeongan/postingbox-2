from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:jungle@sukyeong.o2xkdoo.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def show_articles():
    result = list(db.articles.find({},{'_id':False}))
    return jsonify({'result':'success', 'articles':result})



## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_article():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
		
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        "url" : url_receive,
        "comment" : comment_receive,
        "title" : title,
        "desc" : desc,
        "image" : image
    }

		# 3. mongoDB에 데이터 넣기

    db.articles.insert_one(doc)
    
    return jsonify({'result':'success','msg':'포스팅 성공!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)