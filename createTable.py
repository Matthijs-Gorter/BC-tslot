import sqlite3

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
