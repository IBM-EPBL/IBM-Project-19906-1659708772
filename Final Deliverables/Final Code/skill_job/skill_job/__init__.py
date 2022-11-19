from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.instance_path = 'skill_job/'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from skill_job import routes
with app.app_context():
    db.create_all()
    db.session.commit()    # <- Here commit changes to database
'''
try:
	#os.mkdir(os.path.join(app.root_path, 'static', 'location_pics'))
except:
	pass

'''