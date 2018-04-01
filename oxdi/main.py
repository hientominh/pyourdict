import datetime
import sqlite3

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


app = Flask(__name__)


conn = sqlite3.connect('oxdi.db')
conn.execute('CREATE TABLE IF NOT EXISTS words (time timestamp, word text, means text);')
conn.close()


def get_means_from_oxford_eng_dict(word):
    URL_FMT = 'https://en.oxforddictionaries.com/definition/{}'
    url = URL_FMT.format(word)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    # TODO handle all other gramb (when it is verb / noun ...)
    one = soup.find('section', attrs={'class': 'gramb'})
    means = [i.get_text() for i in one.findAll('span', attrs={'class': 'ind'})]
    return means


# For Oxford Eng dict
@app.route('/ox/<word>')
def translate(word):
    now = datetime.datetime.utcnow()

    means = get_means_from_oxford_eng_dict(word)

    with sqlite3.connect('oxdi.db') as conn:
        conn.execute('INSERT INTO words(time, word, means) VALUES (?, ?, ?);', (now, word, '\n'.join(means)))

    return render_template('meaning.html', means=means, word=word)


@app.route('/')
def index():
    with sqlite3.connect('oxdi.db') as conn:
        conn.row_factory = sqlite3.Row
        words = [(row['time'], row['word'], row['means']) for row in conn.execute('SELECT * FROM words;')]

    return render_template('index.html', words=words)


if __name__ == "__main__":
    app.run(debug=True)
