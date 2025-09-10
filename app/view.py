from app import app, db
from flask import render_template, request, redirect, url_for
from app.forms import LoginForm, BookForm, SignInForm, StudentForm, LoanForm
from app.models import Student, Book, Loan
from flask_login import login_user, logout_user, current_user, login_required 

@app.route('/', methods = ['GET', 'POST'])
def homepage():

    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    return render_template('index.html', form=form)


@app.route('/livro/', methods=['POST', 'GET'])
@login_required
def bookRegister():

    form = BookForm()
    
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('livro.html', form=form)


@app.route('/livro/lista/')
@login_required
def bookList():
    
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')

    dados = Book.query.order_by('id')
    if pesquisa != '':
        dados = dados.filter_by(title=pesquisa)
    context = {'dados': dados.all()}

    return render_template('livroLista.html', context=context)


@app.route('/livro/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def bookEdit(id):

    form = BookForm()

    book = Book.query.get_or_404(id)  # Busca o empréstimo pelo ID
    if form.validate_on_submit():

        # Atualiza os campos do empréstimo
        book.title = form.title.data
        book.author = form.author.data
        book.publisher = form.publisher.data
        book.publiYear = form.publiYear.data
        book.genre = form.genre.data
        book.availNumber = form.availNumber.data
        book.totalNumber = form.totalNumber.data
        db.session.commit()

        return redirect(url_for('bookList'))  # redireciona de volta pra lista

    # Preenche os campos do form com os valores antigos
    form.title.data = book.title 
    form.author.data = book.author
    form.publisher.data = book.publisher
    form.publiYear.data = book.publiYear
    form.genre.data = book.genre
    form.availNumber.data = book.availNumber
    form.totalNumber.data = book.totalNumber

    return render_template('livroEditar.html', form=form, book=book)


@app.route('/livro/excluir/<int:id>', methods=['POST'])
@login_required
def bookDelete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('bookList'))


@app.route('/cadastro/', methods = ['GET', 'POST'])
def cadastro():
    form = SignInForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)


@app.route('/aluno/', methods=['GET', 'POST'])
@login_required
def studentRegister():

    form = StudentForm()

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('alunos.html', form=form)

@app.route('/aluno/lista/')
@login_required
def studentList():
    
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')

    dados = Student.query.order_by('name')
    if pesquisa != '':
        dados = dados.filter_by(name=pesquisa)
    context = {'dados': dados.all()}

    return render_template('alunosLista.html', context=context)


@app.route('/aluno/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def studentEdit(id):
    form = StudentForm()

    student = Student.query.get_or_404(id)  # Busca o empréstimo pelo ID
    if form.validate_on_submit():

        # Atualiza os campos do empréstimo
        student.name = form.name.data
        student.registration = form.registration.data
        db.session.commit()

        return redirect(url_for('studentList'))  # redireciona de volta pra lista

    # Preenche os campos do form com os valores antigos
    form.name.data = student.name
    form.registration.data = student.registration

    return render_template('alunosEditar.html', form=form, student=student)


@app.route('/aluno/excluir/<int:id>', methods=['POST'])
@login_required
def studentDelete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('studentList'))



@app.route('/emprestimo/', methods=['POST', 'GET'])
@login_required
def loanRegister():

    form = LoanForm()

    if form.validate_on_submit():
        student = Student.query.get(form.loanStudent.data)
        book = Book.query.get(form.loanBook.data)

        if not student:
            raise ValueError("Aluno não encontrado")
        if not book:
            raise ValueError("Livro não encontrado")
        form.save()
        return redirect(url_for('homepage'))
    return render_template('emprestimo.html', form=form)


@app.route('/emprestimo/lista/')
@login_required
def loanList():
    
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    
    dados = Loan.query.order_by('id')
    if pesquisa != '':
        dados = dados.filter_by(loanStudent=pesquisa)
    context = {'dados': dados.all()}

    return render_template('emprestimoLista.html', context=context)


@app.route('/emprestimo/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def loanEdit(id):
    form = LoanForm()

    loan = Loan.query.get_or_404(id)  # Busca o empréstimo pelo ID
    if form.validate_on_submit():
        student = Student.query.get(form.loanStudent.data)
        book = Book.query.get(form.loanBook.data)

        if not student:
            raise ValueError("Aluno não encontrado")
        if not book:
            raise ValueError("Livro não encontrado")

        # Atualiza os campos do empréstimo
        loan.loanStudent = form.loanStudent.data
        loan.loanBook = form.loanBook.data
        loan.status = form.status.data
        db.session.commit()

        return redirect(url_for('loanList'))  # redireciona de volta pra lista

    # Preenche os campos do form com os valores antigos
    form.loanStudent.data = loan.loanStudent
    form.loanBook.data = loan.loanBook
    form.status.data = loan.status

    return render_template('emprestimoEditar.html', form=form, loan=loan)


@app.route('/emprestimo/excluir/<int:id>', methods=['POST'])
@login_required
def loanDelete(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    return redirect(url_for('loanList'))



@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))