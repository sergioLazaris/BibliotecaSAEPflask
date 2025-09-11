from app import db
from datetime import datetime, timedelta
from flask_login import UserMixin

def one_week_from_now():
    return datetime.now() + timedelta(weeks=1)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    publiYear = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String, nullable=False)
    availNumber = db.Column(db.Integer, nullable=False)
    totalNumber = db.Column(db.Integer, nullable=False)

class Student(db.Model):
    name = db.Column(db.String, nullable = False)
    registration = db.Column(db.Integer, primary_key = True)

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loanBook = db.Column(db.Integer, db.ForeignKey('book.id', name='fk_loan_book'))
    loanStudent = db.Column(db.Integer, db.ForeignKey('student.registration', name='fk_loan_student'))
    returnLimit = db.Column(db.DateTime, default=one_week_from_now)
    loanDate = db.Column(db.DateTime, default=datetime.now)
    returnDate = db.Column(db.DateTime, default=None)
    status = db.Column(db.String, default='Emprestado')

    student = db.relationship("Student", backref="loans")
    book = db.relationship("Book", backref="loans")

class LoanEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'))
    event_type = db.Column(db.String, nullable=False)
    event_date = db.Column(db.DateTime, default=datetime.now)
    book_title = db.Column(db.String, nullable=False)     
    student_name = db.Column(db.String, nullable=False)   

    loan = db.relationship("Loan", backref="events")
