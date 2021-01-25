from sweater import app, db

from sweater.routes import *

if __name__ == '__main__':
    db.create_all()
    app.run()
