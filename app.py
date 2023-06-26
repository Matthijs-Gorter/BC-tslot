# pyright: reportMissingImports=false

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define a dictionary of valid credentials for the admin dashboard
valid_credentials = {
    'admin': 'password123',
    'matthijs' : '12345678'
}

def initialize_database():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    content TEXT NOT NULL,
    image_url TEXT,
    call_to_action_button TEXT,
    call_to_action_link TEXT
)''')


    conn.commit()
    conn.close()

# Home route - accessible by all users
@app.route('/')
def home():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news_articles ORDER BY id DESC')
    articles = c.fetchall()
    conn.close()

    logged_in = 'logged_in' in session and session['logged_in']

    
    return render_template('home.html', articles=articles, logged_in=logged_in)


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
            return redirect(url_for('admin_dashboard'))  # Modified endpoint here
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

# Admin dashboard route - requires authentication
@app.route('/admin')  # Modified route here
def admin_dashboard():
    # Check if the user is logged in
    if 'logged_in' in session and session['logged_in'] and 'username' in session:
        # Display the admin dashboard
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
        title = request.form['title']
        date = request.form['date']
        content = request.form['content']
        image_url = request.form['image_url']
        call_to_action_button = request.form['call_to_action_button']
        call_to_action_link = request.form['call_to_action_link']

        conn = sqlite3.connect('news.db')
        c = conn.cursor()
        c.execute('INSERT INTO news_articles (title, date, content, image_url, call_to_action_button, call_to_action_link) VALUES (?, ?, ?, ?, ?, ?)', (title, date, content, image_url, call_to_action_button, call_to_action_link))
        conn.commit()
        conn.close()

        # Redirect to the article preview page
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)

