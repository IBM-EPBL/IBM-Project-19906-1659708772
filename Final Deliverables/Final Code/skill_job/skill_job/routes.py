from flask import render_template, url_for, flash, redirect, request
from skill_job import app, db, bcrypt
from skill_job.forms import RegistrationForm, LoginForm, JobPost, SeekerDetails, SearchForm
from skill_job.models import User, Employer, Seeker, Posts, Skills
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os, time
from functools import wraps

Admin_Login = False

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

@app.route("/user_operation", methods=['GET', 'POST'])
@login_required()
def user_operation():
    print('current_user', current_user, current_user.id)
    seeker_info = Seeker.query.filter_by(user_id=current_user.id).first()
    print('seeker_info', seeker_info)
    if not seeker_info:
        add_seeker = Seeker(user_id=current_user.id)
        db.session.add(add_seeker)
        db.session.commit()
        seeker_info = add_seeker
    
    all_posts = Posts.query.all()

    all_skills = Skills.query.with_entities(Skills.skill_name).all()
    all_skills = [i[0] for i in all_skills]
    print('all_skills', all_skills)

    all_company = Employer.query.with_entities(Employer.employer_name).all()
    print('all_company1', all_company)
    all_company = [i[0] for i in all_company]
    print('all_company', all_company)
    
    if seeker_info:
        intrested_skills = seeker_info.skills
        if intrested_skills:
            intrested_skills = intrested_skills.split(',')
            print('intrested_skills', intrested_skills)
            intrested_skills = list(filter(None, intrested_skills))
            print('intrested_skills', intrested_skills)
            skills_to_update = ','.join([all_skills[int(skill)-1] for skill in intrested_skills])
        else:
            intrested_skills = ''
            skills_to_update = ''

        if seeker_info.intrested_companies:
            intrested_companies = seeker_info.intrested_companies
            intrested_companies = intrested_companies.split(',')
            intrested_companies = list(filter(None, intrested_companies))
            print('skills1', intrested_companies)
            company_to_update = []
            for intr in intrested_companies:
                company_to_update.append(Employer.query.filter_by(user_id=intr).first().employer_name)
            company_to_update = ','.join(company_to_update)
        else:
            intrested_companies = ''
            company_to_update = ''
        if seeker_info.location:
            intrested_location = seeker_info.location
        else:
            intrested_location = ''
    else:
        intrested_companies = []
        company_to_update = ''
        skills_to_update = ''
        intrested_location = ''

    share_post = []

    for post in all_posts:
        print('p2', post)
        post_skills = post.skills_needed
        post_skills = post_skills.split(',')
        post_skills = list(filter(None, post_skills))
        skills_needed = []
        for s in post_skills:
            skills_needed.append(Skills.query.filter_by(id=s).first().skill_name)
        post_company = User.query.filter_by(id=post.user_id).first()
        if len(intrested_companies) > 0:
            if current_user.name in intrested_companies:
                share_post.append([post_company.name, post.job_title, ','.join(skills_needed), post.location])
        
        for post_skill in post_skills:
            if post_skill in intrested_skills:
                share_post.append([post_company.name, post.job_title, ','.join(skills_needed), post.location, post.id])

    share_post = sorted(share_post)
    print('share_post', share_post)

    form = SeekerDetails()
    if form.validate_on_submit():
        location_data = form.location.data
        company_data = form.company.data.split(',')
        skills_data = form.skills.data.split(',')
        print('get_data', location_data, skills_data, company_data)

        for i in skills_data:
            if i not in all_skills:
                add_skill = Skills(skill_name=i)
                db.session.add(add_skill)
                db.session.commit()
            else:
                add_skill = Skills.query.filter_by(skill_name=i).first()

            if not seeker_info.skills:
                temp = ''
            else:
                temp = seeker_info.skills
            skill_update = temp+','+str(add_skill.id)
            db.session.commit()

        for i in company_data:
            is_company = Employer.query.filter_by(employer_name=i).first()
            if is_company:
                company_id = is_company.user_id
                if not seeker_info.intrested_companies:
                    temp1 = ''
                else:
                    temp1 = seeker_info.intrested_companies
                print('temp1', temp1)
                company_update = temp1+','+str(company_id)
                db.session.commit()
            else:
                company_update = ''

        seeker_info.location = location_data
        seeker_info.intrested_companies = company_update
        seeker_info.skills = skill_update
        db.session.commit()
        flash('Profile Updated!', 'success')
    form1 = SearchForm()
    return render_template('user_operation.html', title="Seeker Dashboard", share_post=share_post, 
        form=form, skills_to_update=skills_to_update, company_to_update=company_to_update,
        intrested_location=intrested_location, form1=form1)

@app.route('/intrested_job/<int:post_id>', methods=['GET', 'POST'])
def intrested_job(post_id):
    print('current_user', current_user, current_user.id)
    seeker_info = Seeker.query.filter_by(user_id=current_user.id).first()
    post = Posts.query.filter_by(id=int(post_id)).first()
    print('post', post, post.seekers)
    if not post.seekers:
        temp1 = ''
    else:
        temp1 = post.seekers
    temp1 += ','
    temp1 += str(seeker_info.user_id)
    post.seekers = temp1
    db.session.commit()
    flash('Job Applied!', 'success')
    return redirect(url_for('user_operation'))

@app.route('/employer_operation', methods=['GET', 'POST'])
@login_required()
def employer_operation():
    form = JobPost()
    if form.validate_on_submit():
        all_skills = Skills.query.with_entities(Skills.skill_name).all()
        all_skills = [i[0] for i in all_skills]
        print('all_skills', all_skills)
        
        job_title = form.job_title.data
        skills_needed = form.skills_needed.data
        skills_needed = skills_needed.split(',')
        location = form.location.data

        print('input', job_title, skills_needed, location, form.skills_needed.data)
        save_skill = []
        for skill in skills_needed:
            print('a', skill)
            if skill not in all_skills:
                print('>', skill)
                add_skill = Skills(skill_name=skill.lower())
                db.session.add(add_skill)
                db.session.commit()
                print('skill added', add_skill, add_skill.id)
                save_skill.append(add_skill.id)
            else:
                skill_infor = Skills.query.filter_by(skill_name=skill).first()
                print('skill added1', skill_infor, skill_infor.id)
                save_skill.append(skill_infor.id)

        print('#####', job_title, location, save_skill)
        print(type(','.join([str(ss) for ss in save_skill])), ','.join([str(ss) for ss in save_skill]))
        add_post = Posts(user_id=current_user.id, job_title=job_title, location=location, skills_needed=','.join([str(ss) for ss in save_skill]))
        flash('Job is Posted!', 'success')     
        db.session.add(add_post)
        db.session.commit()
        
    all_posts = Posts.query.filter_by(user_id=current_user.id).all()
    all_seekers = Seeker.query.all()
    print('all_posts', all_posts)
    share_post = []
    all_skills = Skills.query.with_entities(Skills.skill_name).all()
    all_skills = [i[0] for i in all_skills]
    print('all_skills', all_skills)
    for post in all_posts:
        post_skill = post.skills_needed
        post_skill = post_skill.split(',')
        print('post_skill', post.skills_needed, post_skill)
        post_skill = list(filter(None, post_skill))
        post_skill = [all_skills[int(i)-1] for i in post_skill]

        post_seekers = []
        if post.seekers:
            post_seekers = post.seekers.split(',')
        seeker_info = []

        for seeker_id in post_seekers:
            seeker_user_info = User.query.filter_by(id=seeker_id).first()
            seeker_skills = []
            if seeker_user_info:
                seeker_name = seeker_user_info.name
                seeker_email = seeker_user_info.email
                seeker_contact_no = seeker_user_info.contact_no

                seeker_skill_sets = Seeker.query.filter_by(user_id=seeker_id).first()
                if seeker_skill_sets:
                    seeker_skills = seeker_skill_sets.skills
                    seeker_skills = seeker_skills.split(',')
                    print('seeker_skills', seeker_skills)
                    seeker_skills = list(filter(None,seeker_skills))
                    seeker_skills = [all_skills[int(i)-1] for i in seeker_skills]
                seeker_info.append([seeker_name, seeker_email, seeker_contact_no, seeker_skills])

        skills_needed = []
        print('post.skills_needed', post.skills_needed)
        for i in post_skill:
            skills_needed.append(i)

        share_post.append([post.user_id, post.job_title, ','.join(skills_needed), post.location, post.id, seeker_info])

    return render_template('employer_operation.html', form=form, title="Emmployer",
                            share_post=share_post,
        )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


