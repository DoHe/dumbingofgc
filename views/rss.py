from feedgen.feed import FeedGenerator
from flask import Response
from data import datastore

TEMPLATE = """
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mobile of age - {title}</title>
    <link rel="shortcut icon" type="image/png" href="https://dumbingofgc.uc.r.appspot.com/static/favicon.ico" />
</head>

<body>
    <h1>
        <a href="/?c={id}">{title}</a>
    </h1>
    <img src="{image}" alt="{alt}" title="{alt}" class="webfeedsFeaturedVisual ">
    <p>{alt}</p>
</body>

</html>
"""


def create_feed():
    fg = FeedGenerator()
    fg.id('https://dumbingofgc.uc.r.appspot.com/rss')
    fg.title('Mobile of Age')
    fg.author({'name': 'Dom', 'email': 'dom@whatevs.de'})
    fg.link(href='https://dumbingofgc.uc.r.appspot.com/', rel='alternate')
    fg.logo('https://dumbingofgc.uc.r.appspot.com/static/favicon.ico')
    fg.subtitle('Dumbing of Age in mobile friendly')
    fg.link(href='https://dumbingofgc.uc.r.appspot.com/rss', rel='self')
    fg.language('en')
    return fg


def add_field(id, comic, fg):
    fe = fg.add_entry()
    fe.id(id)
    fe.title(comic.get('title'))
    fe.link(href=f"https://dumbingofgc.uc.r.appspot.com/?c={id}")
    fe.published(comic.get("date") + "T00:00:00+00:00")
    fe.description(TEMPLATE.format(
        title=comic.get("title"),
        id=id,
        image=comic.get("image"),
        alt=comic.get("alt"),
    ))


def view():
    feed = create_feed()

    comics = datastore.fetch_most_recent_comic(limit=30)
    for comic in comics:
        add_field(comic.id, comic.to_dict(), feed)
    rss = feed.rss_str(pretty=True)
    return Response(rss, mimetype=' application/xml')
