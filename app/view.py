from app import app, db
from flask import render_template, request, redirect, url_for
from app.forms import LoginForm, BookForm, SignInForm, StudentForm, LoanForm
from flask_login import login_user, logout_user, current_user, login_required 

@app.route('/', methods = ['GET', 'POST'])
def homepage():

    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    return render_template('index.html', form=form)

@app.route('/livro/')
@login_required
def bookRegister():

    form = BookForm()
    
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('livro.html', form=form)

@app.route('/cadastro/', methods = ['GET', 'POST'])
def cadastro():
    form = SignInForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)

@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))