from firebase_admin import firestore
from data import DB


def store_comic(title):
    id = u"1232349234932"
    doc_ref = DB.collection(u'comics').document(id)
    doc_ref.set({
        u'title': title,
        u'url': u'Lovelace',
        u'image': u'Lovelace',
        u'alt': u'Lovelace',
        u'date': u'Lovelace'
    })


def fetch_most_recent_comic(limit=30):
    comics_ref = DB.collection(u'comics')
    query = comics_ref.order_by("date").limit_to_last(limit)
    return query.get()
