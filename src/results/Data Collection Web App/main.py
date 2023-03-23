from flask import Flask
import os
from application.config import *

app = None
def create_app():
	app = Flask(__name__, template_folder = "templates")
	app.app_context().push()
	if os.getenv("DEPLOYMENT_ENV") == "Development":
		app.config.from_object(DEVELOPMENT)
	else: 
		app.config.from_object(PRODUCTION)
	return app

app = create_app()
if __name__ == "__main__":
	from application.controllers import *
	app.run()