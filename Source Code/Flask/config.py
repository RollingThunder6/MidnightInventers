class Config():
	"""Configuration settings"""
	SECRET_KEY = "rollingthunder6"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	def init_app(app):
		pass		

class development_config(Config):
	"""configuration in development mode"""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/flask"

config = {
	'default': development_config
}