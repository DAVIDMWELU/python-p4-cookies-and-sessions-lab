#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'  # Necessary for session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Route to clear session (reset page views)
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Route to list all articles
@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return make_response(
        jsonify([article.to_dict() for article in articles]),
        200
    )

# Route to view individual article with paywall logic
@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize or increment page view counter
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()
        if article:
            return make_response(jsonify(article.to_dict()), 200)
        else:
            return make_response(jsonify({'message': 'Article not found'}), 404)
    else:
        return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)

if __name__ == '__main__':
    app.run(port=5555)
