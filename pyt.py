from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, Text, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/pyt.db'
db = SQLAlchemy(app)


class Member(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    finance = relationship('Finance', backref='by', lazy='dynamic')
    meals = relationship('Meal', backref='meals', lazy='dynamic')


class Meal(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    member = Column(String, ForeignKey('member.name'), nullable=False)
    number = Column(Integer, nullable=False)
    notes = Column(Text)


class Finance(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    debit = Column(Integer, default=0)
    credit = Column(Integer, default=0)
    member = Column(String, ForeignKey('member.name'))
    notes = Column(Text)

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)

api_manager.create_api(Member, methods=['GET', 'POST', 'PUT', 'DELETE'])

api_manager.create_api(Meal, methods=['GET', 'POST', 'PUT', 'DELETE'],  exclude_columns=['meals'])

api_manager.create_api(Finance, methods=['GET', 'POST', 'PUT', 'DELETE'])


@app.route('/')
def index():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(debug=True)
