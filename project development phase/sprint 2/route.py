def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print('decorated_view')
            if not current_user.is_authenticated:
               print('not is_authenticated')
               return app.login_manager.unauthorized()
            urole = current_user.role
            print('urole', urole)
            if ((urole != role) and (role != "ANY")):
                print('unauthorized')
                return app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
       return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password,
            contact_no=form.contact_no.data, gender=form.gender.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        print(user)
        if form.role.data=='Employer':
            add_employer = Employer(user_id=user.id, employer_name=form.name.data)
            db.session.add(add_employer)
            db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_operation'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print("Login Success", user)
            next_page = request.args.get('next')
            if user.role == 'Seeker':
                return redirect(next_page) if next_page else redirect(url_for('user_operation'))
            if user.role == 'Employer':
                return redirect(next_page) if next_page else redirect(url_for('employer_operation'))
            #return redirect(url_for('user_operation'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


