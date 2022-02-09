from webapp import create_app
from webapp.news.parsers import habr

app = create_app()
with app.app_context():
    habr.get_habr_snippets()