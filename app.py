from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    call_to_action_button = db.Column(db.Text)
    call_to_action_link = db.Column(db.Text)
    __tablename__ = 'news_articles'

# Define a dictionary of valid credentials for the admin dashboard
valid_credentials = {
    'admin': 'password123',
    'matthijs': '12345678'
}

# Home route - accessible by all users


@app.route('/')
def home():
    articles = NewsArticle.query.order_by(NewsArticle.id.desc()).all()
    return render_template('home.html', 
                           articles=articles, 
                           logged_in='logged_in' in session and session['logged_in'] and 'username' in session, 
                           username = 'username' in session and session['username'])


# Login route - displays login form and processes login requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided credentials are valid
        if username in valid_credentials and valid_credentials[username] == password:
            session['logged_in'] = True
            session['username'] = username
            # Modified endpoint here
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Admin dashboard route - requires authentication


@app.route('/admin')
def admin_dashboard():
    if 'logged_in' in session and session['logged_in'] and 'username' in session:
        return render_template('admin.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Logout route - clears the session and redirects to the login page


@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

# Add article route - allows the admin to add a news article


@app.route('/add_article', methods=['POST'])
def add_article():
    if 'logged_in' in session and session['logged_in'] and 'username' in session:
        article = NewsArticle(
            title=request.form['title'],
            date=request.form['date'],
            content= request.form['content'],
            image_url=request.form['image_url'],
            call_to_action_button=request.form['call_to_action_button'],
            call_to_action_link=request.form['call_to_action_link']
        )

        db.session.add(article)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'logged_in' in session and session['logged_in'] and 'username' in session:
        if request.method == 'GET':
            article = NewsArticle.query.get(article_id)
            print(article.title)
            if article:
                return render_template('edit_article.html', article=article)
            else:
                return "Article not found"        
        elif request.method == 'POST':
            article = NewsArticle.query.get(article_id)
            article.title = request.form['title']
            article.date = request.form['date']
            article.content = request.form['content']
            article.image_url = request.form['image_url']
            article.call_to_action_button = request.form['call_to_action_button']
            article.call_to_action_link = request.form['call_to_action_link']

            db.session.commit()

            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/delete_article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if 'logged_in' in session and session['logged_in'] and 'username' in session:
        db.session.delete(NewsArticle.query.get(article_id))
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))



@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80, debug=True)
