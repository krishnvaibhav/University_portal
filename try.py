def login_page():
    form = forms.LoginForm()
    error = ""
    if form.validate_on_submit():
        user_name_login = form.Username.data
        password_login = form.Password.data
        member = form.member.data
        if member == 'admin':
            cur_user = Admin.query.filter_by(Username=user_name_login).first()
        elif member == "student":
            cur_user = Student.query.filter_by(RollNo=user_name_login).first()
        elif member == "teacher":
            cur_user = Teacher.query.filter_by(Username=user_name_login).first()

            if cur_user:
                if bcrypt.check_password_hash(cur_user.Password, password_login):
                    error = ""
                    login_user(cur_user)
                    session['user'] = member
                    session['user-name'] = cur_user.Name
                    return redirect(url_for(f'{member}_login'))
                else:
                    error = "incorrect password"
            else:
                error = "No such user"
