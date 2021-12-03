from flask import Flask, render_template

from views import index, rss, tasks

app = Flask(__name__)


app.add_url_rule('/', 'index', view_func=index.view)
app.add_url_rule('/rss', 'rss', view_func=rss.view)
app.add_url_rule('/tasks/scrape', 'scrape', view_func=tasks.scrape)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
