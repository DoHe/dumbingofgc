from flask import render_template, request

from data import datastore
from constants import COMIC_URL


def view():
    c = request.args.get('c')
    if c is None:
        comics = datastore.fetch_most_recent_comic(limit=1)
        if len(comics) == 0:
            return render_template('index.html')
        comic = comics[0].to_dict()
    else:
        comic = datastore.fetch_comic(id=c).to_dict()
        if comic is None:
            return render_template('index.html')

    original_url = COMIC_URL + comic.get("url", "")
    return render_template(
        'index.html',
        comic=comic,
        original_url=original_url
    )
