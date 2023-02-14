import datetime
import io
import time
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, session, jsonify , send_file
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import json
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
import Search_Engine
import forms
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import sys
from profanity_check import predict
import smtplib

sender_email = "anonymousrobot974@gmail.com"

with open('config.json', 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "My key"

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'anonymousrobot974@gmail.com'
app.config['MAIL_PASSWORD'] = 'iebtzxtcfwmtdnds'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'


@login_manager.user_loader
def load_user(id):
    if 'user' in session:
        if session['user'] == "admin":
            return Admin.query.get(int(id))
        elif session['user'] == "student":
            return Student.query.get(int(id))
        elif session['user'] == "teacher":
            return Teacher.query.get(int(id))


class Admin(db.Model, UserMixin):
    AID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Username = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.AID


class Student(db.Model, UserMixin):
    SID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Username = db.Column(db.String(100), nullable=False, unique=True)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Mobile = db.Column(db.String(100), nullable=False, unique=True)
    Class = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.SID


class StudentPersonal(db.Model, UserMixin):
    SPID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), nullable=False)
    Marks_10 = db.Column(db.Integer, nullable=False)
    Marks_12 = db.Column(db.Integer, nullable=False)
    Father_Name = db.Column(db.String(100), nullable=False)
    Mother_Name = db.Column(db.String(100), nullable=False)
    City = db.Column(db.String(100), nullable=False, unique=True)
    State = db.Column(db.String(100), nullable=False, unique=True)
    Country = db.Column(db.String(100), nullable=False)
    Local_Guardian = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.SPID


class Teacher(db.Model, UserMixin):
    TID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Username = db.Column(db.String(100), nullable=False, unique=True)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Mobile = db.Column(db.String(100), nullable=False, unique=True)
    Class = db.Column(db.String(100), nullable=False)
    Salary = db.Column(db.Integer, nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    Class1 = db.Column(db.String(100), nullable=False)
    Class2 = db.Column(db.String(100), nullable=False)
    Class3 = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.TID


class TeacherPersonal(db.Model, UserMixin):
    TPID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), nullable=False, unique=True)
    City = db.Column(db.String(100), nullable=False, unique=True)
    State = db.Column(db.String(100), nullable=False, unique=True)
    Country = db.Column(db.String(100), nullable=False)
    Qualification = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.TPID


class Announcement(db.Model, UserMixin):
    ANID = db.Column(db.Integer, primary_key=True)
    TEXT = db.Column(db.String(200), nullable=False)
    Class = db.Column(db.String(100), nullable=False)
    Date_time = db.Column(db.DateTime)
    TName = db.Column(db.String(100),nullable = False)

    def get_id(self):
        return self.ANID

class Notes(db.Model,UserMixin):
    NID = db.Column(db.Integer, primary_key=True)
    Class = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.String(200), nullable=False)
    TName = db.Column(db.String(100),nullable = False)
    data = db.Column(db.LargeBinary,nullable=False)
    filename = db.Column(db.String(100),nullable = False)
    type = db.Column(db.String(100),nullable = False)
    upload_date = db.Column(db.Date,nullable=False)

    def get_id(self):
        return self.NID


@app.route('/', methods=['GET', 'POST'])
def login_page():
    form = forms.LoginForm()
    error = ""
    if form.validate_on_submit():
        user_name_login = form.Username.data
        password_login = form.Password.data
        member = form.member.data
        cur_user = getattr(sys.modules[__name__], member.capitalize()).query.filter_by(Username=user_name_login).first()
        if cur_user:
            if bcrypt.check_password_hash(cur_user.Password, password_login):
                error = ""
                login_user(cur_user)
                session['user'] = member
                session['user-name'] = cur_user.Name
                session['Username'] = cur_user.Username
                return redirect(url_for(f'{member}_login'))
            else:
                error = "incorrect password"
        else:
            error = "No such user"

    return render_template('login.html', error=error, form=form)


@app.route('/admin-page', methods=['GET', 'POST'])
@login_required
def admin_login():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "admin":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))

    formst = forms.SearchAdminStudent()
    formth = forms.SearchAdminTeacher()
    search_text_st = formst.Username_st.data
    search_text_th = formth.Username_th.data
    if search_text_st != None:
        students = Student.query.filter(Student.Username.like(f"{search_text_st}%"))
    else:
        students = Student.query.all()
    if search_text_th != None:
        teachers = Teacher.query.filter(Teacher.Username.like(f"{search_text_th}%"))
    else:
        teachers = Teacher.query.all()
    return render_template('admin_index.html', name=name, students=students, teachers=teachers, formst=formst,
                           formth=formth)


@app.route('/student-page', methods=['GET', 'POST'])
@login_required
def student_login():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "student":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
    form = forms.PersonalDetails()

    class_name = user = getattr(sys.modules[__name__], session['user'].capitalize())
    personal_class_name = getattr(sys.modules[__name__], f"{session['user'].capitalize()}Personal")
    details = class_name.query.filter_by(Username=session['Username']).first()
    all_user_details = db.session.query(class_name, personal_class_name).filter_by(Username=session['Username']) \
        .outerjoin(personal_class_name, class_name.Username == personal_class_name.Username).first()
    if all_user_details[1] == None:
        if form.validate_on_submit():
            new = personal_class_name(Username=details.Username, Marks_10=form.Marks_10.data,
                                      Marks_12=form.Marks_12.data
                                      , City=form.City.data, State=form.State.data, Country=form.Country.data,
                                      Local_Guardian=form.Local_Guardian.data, Father_Name=form.Father_Name.data,
                                      Mother_Name=form.Mother_Name.data)
            db.session.add(new)
            db.session.commit()
            return redirect(url_for('student_login'))
        return render_template('personal_details.html', form=form, member=session['user'])

    announcement =  db.session.query(class_name,Announcement).filter_by(Class=details.Class).join(class_name,Announcement.Class==class_name.Class).all()

    return render_template('student_index.html', name=name, user=all_user_details,announcements=announcement)

@app.route('/download-notes')
@login_required
def view_notes():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "student":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
    student_query = Student.query.filter_by(Username=session['Username']).first()
    student_class = student_query.Class
    count_notes_class = Notes.query.filter_by(Class=student_class).count()
    print(count_notes_class)
    all_notes = db.session.query(Student, Notes).filter_by(Class=student_class)\
        .join(Notes, Student.Class == Notes.Class).all()
    first_notes = all_notes[:count_notes_class]

    return render_template('download_notes.html',notes=first_notes)





@app.route('/upload-notes',methods=['GET','POST'])
@login_required
def upload_notes():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "teacher":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))

    form = forms.notes()
    user = Teacher.query.filter_by(Username=session['Username']).first()
    if form.validate_on_submit():
        data = form.file.data
        selected_class = request.form.get('classes')
        upload = Notes(data=data.read(),Message=form.description.data,Class=selected_class,TName="Messi",type=data.mimetype,filename=data.filename)
        db.session.add(upload)
        # db.session.commit()
        Students = Student.query.filter_by(Class=selected_class).all()
        msg = Message(
            'Material Uploaded !!!!',
            sender=sender_email,
            recipients=[i.Email for i in Students]
        )
        print(msg.recipients)
        msg.body = f'Dear Students material has been uploaded in your portal'
        print(data.mimetype)
        print(data.filename)
        msg.attach(data.filename, data.mimetype, data.read())
        mail.send(msg)
        return redirect(url_for('teacher_login'))

    return render_template('notes.html',form=form,user=user)

@app.route('/download')
def download():
    notes_id = request.args.get('id')
    print(notes_id)
    upload = Notes.query.filter_by(NID=notes_id).first()
    return send_file(io.BytesIO(upload.data),as_attachment=True,download_name=upload.filename,mimetype=upload.type)


@app.route('/teacher-login', methods=['GET', 'POST'])
@login_required
def teacher_login():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "teacher":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
    class_name = user = getattr(sys.modules[__name__], session['user'].capitalize())
    personal_class_name = getattr(sys.modules[__name__], f"{session['user'].capitalize()}Personal")
    all_user_details = db.session.query(class_name, personal_class_name).filter_by(Username=session['Username']) \
        .outerjoin(personal_class_name, class_name.Username == personal_class_name.Username).first()
    form = forms.announcement()
    if form.validate_on_submit():
        text = form.announcement.data
        cur_time = func.now()
        print(cur_time)
        Class = request.form.get('classes')
        tname = session['user-name']
        print(tname)
        new = Announcement(TEXT=text,Class=Class,Date_time=cur_time,TName=tname)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('teacher_login'))

    return render_template('teacher_index.html', name=name, user=all_user_details, form=form)


@app.route('/member-details/add-class', methods=['GET', 'POST'])
@login_required
def add_class():
    error = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "admin":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))

    form = forms.add_class()
    teacher = Teacher.query.filter_by(Username=session['Username']).first()
    if form.validate_on_submit():
        if teacher.Class1 == "":
            teacher.Class1 = form.SEM.data + form.Course.data
            if teacher.Class1 == teacher.Class:
                error = "teacher is already teaching this class"
                teacher.Class1 = ""
            db.session.commit()
        elif teacher.Class2 == "":
            teacher.Class2 = form.SEM.data + form.Course.data
            if teacher.Class2 == teacher.Class or teacher.Class2 == teacher.Class1:
                error = "teacher is already teaching this class"
                teacher.Class2 = ""
            db.session.commit()
        elif teacher.Class3 == "":
            teacher.Class3 = form.SEM.data + form.Course.data
            if teacher.Class3 == teacher.Class or teacher.Class3 == teacher.Class1 or teacher.Class3 == teacher.Class2:
                error = "teacher is already teaching this class"
                teacher.Class3 = ""
            db.session.commit()
        else:
            error = "Already teaching 4 classes cant add more"

    return render_template('update-member.html', add_class=True, form=form, error=error)


@app.route('/student/search-engine', methods=['GET', 'POST'])
@login_required
def search_engine():
    profane = ""
    engine = ""
    search_form = forms.SearchEngine()
    query = search_form.search.data

    if query is not None:
        if predict([query]) == [1]:
            profane = True
            engine = ""
        else:
            profane = False
            engine = Search_Engine.SearchEngine(query.capitalize())

    return render_template('search_engine.html', search=search_form, query=query, engine=engine, profane=profane,
                           member=session['user'])


@app.route('/update-member', methods=['GET', 'POST'])
@login_required
def update_member():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "admin":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
    salary_value = ""
    if 'to-update' in session:
        member = session['to-update']
    else:
        return redirect(url_for('member_details'))
    form = forms.UpdateMember()
    cur_member = getattr(sys.modules[__name__], session['to-update'].capitalize()).query.filter_by(
        Username=session['Username']).first()
    if session['to-update'] == 'Teacher':
        salary_value = cur_member.Salary
    sem_value = cur_member.Class[0]
    mobile_value = cur_member.Mobile
    email_value = cur_member.Email
    if form.validate_on_submit():
        cur_member.Email = form.Email.data
        cur_member.Class = form.SEM.data + cur_member.Class[1:]
        cur_member.Mobile = form.Mobile.data
        if session['to-update'] == 'Teacher':
            cur_member.Salary = form.Salary.data
        db.session.commit()
        return redirect(url_for('admin_login'))
    return render_template('update-member.html', form=form, member=member, sem_value=sem_value,
                           mobile_value=mobile_value
                           , email_value=email_value, salary_value=salary_value, add_class=False)


@app.route('/delete-member')
def delete_member():
    username = request.args.get('user')
    member = request.args.get('member')
    user = getattr(sys.modules[__name__], member).query.filter_by(Username=username).first()
    personal_user = getattr(sys.modules[__name__], f"{member}Personal").query.filter_by(Username=username).first()
    db.session.delete(user)
    db.session.delete(personal_user)
    db.session.commit()
    return redirect(url_for('admin_login'))


@app.route('/make-member', methods=['GET', 'POST'])
@login_required
def create_member():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "admin":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
    global new_member
    form = forms.CreateMember()
    member = request.args.get('member')
    if form.validate_on_submit():
        name = form.Name.data
        sem = form.SEM.data
        course = form.Course.data
        Username = form.Username.data
        mobile = form.Mobile.data
        email = form.Email.data
        salary = form.Salary.data
        class_ = sem + course
        password = bcrypt.generate_password_hash(form.Password.data)

        if member == 'teacher':
            new_member = Teacher(Name=name, Username=Username, Mobile=mobile,
                                 Class=class_, Password=password, Email=email, Salary=salary)
        elif member == 'student':
            new_member = Student(Name=name, Username=Username, Mobile=mobile,
                                 Class=class_, Password=password, Email=email)

        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('admin_login'))
    print('not validated')
    return render_template('make-member.html', form=form, member=member)


@app.route('/member-details')
@login_required
def member_details():
    name = ""
    if "user" in session and "user-name" in session:
        if session['user'] == "admin":
            name = session['user-name']
        else:
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('login_page'))
    session['Username'] = request.args.get('user')
    session['member'] = request.args.get('member')
    class_name = getattr(sys.modules[__name__], session['member'])
    personal_class_name = getattr(sys.modules[__name__], f"{session['member']}Personal")
    all_user_details = db.session.query(class_name, personal_class_name).filter_by(Username=session['Username']) \
        .outerjoin(personal_class_name, class_name.Username == personal_class_name.Username).first()
    session['to-update'] = session['member']
    return render_template('member_details.html', user=all_user_details, member=session['member'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    session.pop('user-name', None)
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# @app.route('/make-admin', methods=['GET', 'POST'])
# def make_admin():
#     form = forms.MakeAdmin()
#     if form.validate_on_submit():
#         username = form.Username.data
#         password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
#         name = form.Name.data
#         new = Admin(Name=name, Username=username, Password=password)
#         db.session.add(new)
#         db.session.commit()
#     return render_template('try.html', form=form)
