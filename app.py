from flask import Flask
from random import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///markers.db'
db = SQLAlchemy(app)

class MarkerList(db.Model):
    id = db.Column(db.String, primary_key = True, default = '*')
    value = db.Column(db.Float, default = 0.0)

    def __init__(self, id, value):
       self.id = id
       self.value = value


markercache = [random() for i in range(0,9)]

def url_list(source, methods=('GET','POST')):
    def decorator(f):
        index = 0
        for entry in source:
            def view_func(entry=entry, **kwargs):
                return f(entry, **kwargs)

            endpoint = '{0}_{1}'.format(f.__name__, entry)
            url = '/{0}'.format(index)

            app.add_url_rule(url,
                             methods=methods,
                             endpoint=endpoint,
                             view_func=view_func)
            index += 1
    return decorator


@url_list(markercache)
def printnumber(entry):
    return str(entry)


if __name__ == "__main__":
    app.run()