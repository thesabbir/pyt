from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from pyt import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/pyt.db'


db = SQLAlchemy(app)


class Member(db.Model):
    id = Column(Integer)
    name = Column(String, primary_key=True)
    funds = relationship('Funds', backref='by', lazy='dynamic')
    meals = relationship('Meal', backref='by', lazy='dynamic')

    def total_funds(self):
        total_funds = 0
        for fund in self.funds:
            total_funds += fund.amount
        return total_funds


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


class Funds(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    amount = Column(Integer, default=0)
    member = Column(String, ForeignKey('member.name'), nullable=False)
    manager = Column(String, ForeignKey('manager.id'), default=0)
    notes = Column(Text)


class Invoice(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    amount = Column(Integer, default=0)
    manager = Column(String, ForeignKey('manager.id'), default=0)
    notes = Column(Text, nullable=False)


class Manager(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Fayez Bhaban")
    funds = relationship('Funds', backref='funds', lazy='dynamic')
    expenses = relationship('Invoice', backref='by', lazy='dynamic')
    meals = relationship('Meal', backref='meals', lazy='dynamic')

    def total_funds(self):
        total_funds = 0
        for fund in self.funds:
            total_funds += fund.amount
        return total_funds

    def total_expense(self):
        total_expense = 0
        for expense in self.expenses:
            total_expense += expense.amount
        return total_expense

    def total_meal(self):
        total_meal = 0
        for meal in self.meals:
            total_meal += meal.number
        return total_meal

    def meal_rate(self):
        meal_rate = self.total_expense() / self.total_meal()
        return meal_rate


db.create_all()