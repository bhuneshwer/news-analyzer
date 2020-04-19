from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from markupsafe import escape
from newspaper import Article
import requests
import nltk


app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/dashboard/<name>')
def dashboard(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('dashboard',name = user))
   else:
      user = request.args.get('name')
      return render_template('login.html')


@app.route('/analyze',methods=['GET'])
def analyze():
    news_url = request.args.get("url")
    if(news_url and len(news_url)):
        article = Article(news_url)
        article.download()
        article.parse()
        nltk.download("punkt")
        article.nlp()
        content = {
            "authors"  : article.authors,
            "publish_date" : article.publish_date,
            "article_image" : article.top_image,
            "article_text" : article.text,
            "article_title" : article.title,
            "article_summary" : article.summary,
            "keywords":article.keywords,
            "tags":article.tags
        }
        return content

    #return render_template('news-summary.html',**content)
 
 # if __name__ == '__main__':
 #   app.run(debug = True)
