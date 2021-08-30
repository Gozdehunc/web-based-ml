from flask import Flask
from flask_sqlalchemy import SQLAlchemy

file_name = "database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




app.config["SECRET_KEY"]="ca018564e168dccf34d52afee5db7427185a8be3dca1440ca0ad03b0665503cd"

db = SQLAlchemy(app)

