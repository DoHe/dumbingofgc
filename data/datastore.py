from firebase_admin import firestore
from data import DB


def id_from_url(url):
    if url is None:
        return None
    return url.replace("/", "__")


def url_from_id(id):
    if id is None:
        return None
    return id.replace("__", "/")


def store_comic(
    url,
    image,
    alt,
    date,
    title,
    previous,
    next,
):
    doc_ref = DB.collection(u'comics').document(id_from_url(url))
    doc_ref.set({
        u'url': url,
        u'title': title,
        u'image': image,
        u'alt':     alt,
        u'date': date,
        u'previous': id_from_url(previous),
        u'next': id_from_url(next),
    })


def fetch_most_recent_comic(limit=30):
    comics_ref = DB.collection(u'comics')
    query = comics_ref.order_by(
        "date",
        direction=firestore.Query.DESCENDING
    ).limit(limit)
    return query.get()


def fetch_comic(id):
    doc = DB.collection(u'comics').document(id).get()
    return doc
