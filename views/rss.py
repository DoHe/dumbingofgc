from feedgen.feed import FeedGenerator
from flask import Response
from data import datastore


def create_feed():
    fg = FeedGenerator()
    fg.id('http://lernfunk.de/media/654321')
    fg.title('Some Testfeed')
    fg.author({'name': 'John Doe', 'email': 'john@example.de'})
    fg.link(href='http://example.com', rel='alternate')
    fg.logo('http://ex.com/logo.jpg')
    fg.subtitle('This is a cool feed!')
    fg.link(href='http://larskiesow.de/test.atom', rel='self')
    fg.language('en')
    return fg


def add_field(comic, fg):
    fe = fg.add_entry()
    fe.id('http://lernfunk.de/media/654321/1')
    fe.title(comic.get('title'))
    fe.link(href="http://lernfunk.de/feed")


def view():
    feed = create_feed()

    comics = datastore.fetch_most_recent_comic(limit=30)
    for comic in comics:
        add_field(comic.to_dict(), feed)
    rss = feed.rss_str(pretty=True)
    return Response(rss, mimetype=' application/xml')
