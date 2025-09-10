from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from app import app, bcrypt, db
from app.models import Employee, Student, Book, Loan


class SignInForm(FlaskForm):
    username = StringField('Nome Completo', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirmation = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    btnSubmit = SubmitField('Cadastrar-se')

    def save(self):
        password = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        user = Employee(
            name=self.username.data, 
            password=password
            )
        
        db.session.add(user)
        db.session.commit()
        return user
    


class LoginForm(FlaskForm):
    username = StringField('Nome Completo', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

    def login(self):
        user = Employee.query.filter_by(name=self.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, self.password.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha incorreta')
        else:
            raise Exception('Usuário não encontrado')
        


class BookForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    publisher = StringField('Editora', validators=[DataRequired()])
    publiYear = StringField('Ano de Publicação', validators=[DataRequired()])
    genre = StringField('Gênero', validators=[DataRequired()])
    availNumber = StringField('Número Disponível', validators=[DataRequired()])
    totalNumber = StringField('Número Total', validators=[DataRequired()])
    btnSubmit = SubmitField('Adicionar Livro')

    def save(self):
        book = Book(
            title=self.title.data,
            author=self.author.data,
            publisher=self.publisher.data,
            publiYear=self.publiYear.data,
            genre=self.genre.data,
            availNumber=self.availNumber.data,
            totalNumber=self.totalNumber.data
        )
        db.session.add(book)
        db.session.commit()



class StudentForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    registration = StringField('Matrícula', validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar Aluno')

    def save(self):
        student = Student(
            name=self.name.data,
            registration=self.registration.data
        )
        db.session.add(student)
        db.session.commit()



class LoanForm(FlaskForm):
    loanBook = StringField('ID do Livro', validators=[DataRequired()])
    loanStudent = StringField('Matrícula do Aluno', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    btnSubmit = SubmitField('Registrar Empréstimo')

    def save(self):
        loan = Loan(
            loanBook=self.loanBook.data,
            loanStudent=self.loanStudent.data,
            status=self.status.data
        )
        db.session.add(loan)
        db.session.commit()


