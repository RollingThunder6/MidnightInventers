import os

class Config():
	"""Configuration settings"""
	SECRET_KEY = "rollingthunder6"

	def init_app(app):
		pass

class development_config(Config):
	"""configuration in development mode"""
	DEBUG = True

class production_config(Config):
	"""configuration in production mode"""
	DEBUG = False
		

config = {
	'production': production_config,
	'development': development_config,
	'default': development_config
}