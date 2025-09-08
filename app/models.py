from app import db
from datetime import datetime, timedelta

def one_week_from_now():
    return datetime.now() + timedelta(weeks=1)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    publiYear = db.Column(db.DateTime, default=datetime.now())
    genre = db.Column(db.String, nullable=False)
    availNumber = db.Column(db.Integer, nullable=False)
    totalNumber = db.Column(db.Integer, nullable=False)

class Student(db.Model):
    name = db.Column(db.String, nullable = False)
    registration = db.Column(db.Integer, primary_key = True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    LoanBook = db.Column(db.ForeignKey('Book.id'))
    LoanStudent = db.Column(db.ForeignKey('Student.registration'))
    returnDate = db.Column(db.DateTime, default=one_week_from_now())
    status = db.Column(db.String, nullable=False)
