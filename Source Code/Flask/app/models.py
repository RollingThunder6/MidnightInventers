from . import db

class Credentials(db.Model):
	"""username and password for system"""
	__tablename__ = "credentials"
	password = db.Column(db.String(20))
	username = db.Column(db.String(20), primary_key=True)