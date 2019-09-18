from flask import Flask
from config import Config
from peewee import SqliteDatabase
# from logging.handlers import RotatingFileHandler
from logging import FileHandler, Formatter, INFO

app = Flask(__name__)
app.config.from_object(Config)
file_handler = FileHandler('logs/app.log')  # RotatingFileHandler
file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.setLevel(INFO)
file_handler.setLevel(INFO)
app.logger.addHandler(file_handler)
db = SqliteDatabase('data.db')

from app import routes, models, errors
from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

app.jinja_env.globals['my_global_var'] = 'my_global_var`s_value'
