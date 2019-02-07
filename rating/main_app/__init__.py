import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


SECRET_KEY = os.urandom(32)

app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
db.app = app
login_manager = LoginManager(app)
csrf = CSRFProtect(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SECRET_KEY'] = SECRET_KEY
migrate = Migrate(app, db)

@app.before_request
def before_request():
    g.user = current_user


manager = Manager(app)
manager.add_command('db', MigrateCommand)

from main_app import views, models
