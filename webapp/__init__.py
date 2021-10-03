from flask import Flask, render_template
from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        page_title = 'Новости Python'
        weahter = weather_by_city('Khabarovsk,Russia')
        news_list = get_python_news()
        return render_template('index.html',page_title=page_title,weahter=weahter,news_list=news_list)
    return app


