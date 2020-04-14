from flask_login import UserMixin 
from app import db, login 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader 
def load_user(id):
    return User.query.get(int(id)) 
    

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    # now = datetime.now()
    # dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    username = db.Column(db.Integer, db.ForeignKey('user.username'))
    landmark = db.Column(db.String(40))
    rating = db.Column(db.Integer)

    def __repr__(self):
        return '<Review by {} on {}>'.format(self.body, self.landmark) 


class Bookmark(db.Model):
	__tablename__ = 'bookmark'
	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
	landmark = db.Column(db.String(40), nullable=False)

	def __repr__(self):
		return '{}'.format(self.landmark)
