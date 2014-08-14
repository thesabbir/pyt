from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, Text, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/pyt.db'
db = SQLAlchemy(app)


class Member(db.Model):
    id = Column(Integer)
    name = Column(String, primary_key=True)
    balances = relationship('Balance', backref='by', lazy='dynamic')
    meals = relationship('Meal', backref='by', lazy='dynamic')

    def total_debit(self):
        total_debit = 0
        for balance in self.balances:
            total_debit += balance.debit
        return total_debit

    def total_credit(self):
        total_credit = 0
        for balance in self.balances:
            total_credit += balance.credit
        return total_credit

    def total_meal(self):
        total_meal = 0
        for meal in self.meals:
            total_meal += meal.number
        return total_meal


class Meal(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    member = Column(String, ForeignKey('member.name'), nullable=False)
    manager = Column(String, ForeignKey('manager.id'), default=0)
    number = Column(Integer, nullable=False)
    notes = Column(Text)


class Balance(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    debit = Column(Integer, default=0)
    credit = Column(Integer, default=0)
    member = Column(String, ForeignKey('member.name'))
    manager = Column(String, ForeignKey('manager.id'), default=0)
    notes = Column(Text)


class Manager(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Fayez Bhaban")
    balances = relationship('Balance', backref='balances', lazy='dynamic')
    meals = relationship('Meal', backref='meals', lazy='dynamic')

    def total_debit(self):
        total_debit = 0
        for balance in self.balances:
            total_debit += balance.debit
        return total_debit

    def total_credit(self):
        total_credit = 0
        for balance in self.balances:
            total_credit += balance.credit
        return total_credit

    def total_meal(self):
        total_meal = 0
        for meal in self.meals:
            total_meal += meal.number
        return total_meal

    def meal_rate(self):
        meal_rate = self.total_credit() / self.total_meal()
        return  meal_rate

db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)

api_manager.create_api(
    Member, methods=['GET', 'POST', 'PUT', 'DELETE'],
    exclude_columns=['meals', 'balances'],
    include_methods=['total_debit', 'total_credit', 'total_meal']
)

api_manager.create_api(
    Meal, methods=['GET', 'POST', 'PUT', 'DELETE'],
    exclude_columns=['by']
)

api_manager.create_api(
    Balance, methods=['GET', 'POST', 'PUT', 'DELETE']
)

api_manager.create_api(
    Manager, methods=['GET'],
    exclude_columns=['meals', 'balances'],
    include_methods=['total_debit', 'total_credit', 'total_meal', 'meal_rate']
)


@app.route('/')
def index():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(debug=True)
