from skill_job import app

if __name__ == '__main__':
    app.run(debug=True)

'''
pip install email_validator
pip install flask_sqlalchemy
pip install flask_wtf
pip install flask_login
pip install flask_bcrypt

'''
'''
from tourist import db
db.create_all()
from tourist.models import Admin
ad = Admin(email="admin@admin.com", password="admin")
db.session.add(ad)
db.session.commit()
'''