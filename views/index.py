from flask import render_template

from data import datastore


def view():
    comics = datastore.fetch_most_recent_comic(limit=1)
    comic = None
    if len(comics) > 0:
        comic = comics[0]

    return render_template('index.html', comic=comic.to_dict())
