from flask import Flask
from flask import render_template,redirect,url_for
from flask import request
from markupsafe import escape
from newspaper import fulltext
from newspaper import Article
import requests
import nltk
import ssl


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

app = Flask(__name__)




@app.route('/')
def index():
    return 'Welcome to news-analyzer api.'


@app.route('/hello/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)


@app.route("/get_html",methods=['GET'])
def get_html():
    news_url = request.args.get("url")
    try:
      if(news_url and len(news_url)):
        html = requests.get(news_url).text
        return render_template('news-summary.html', news_html=fulltext(html))
    except Exception as e:
      return render_template('news-summary.html', news_html=e)


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
            "keywords":article.keywords
        }
        return content

 
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, debug=True, port=5000)
