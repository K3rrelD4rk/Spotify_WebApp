from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy import false, true
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long!', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters long', category='error')
        else:
            new_user = User( Username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            flash('Account created!', category='success')
            return redirect('/auth')
    
    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful', category='success')
                login_user(user, remember=False)
                session['logged_in'] = True
                return redirect('/auth')
            else:
                flash('Password incorrect', category='error')
        else:
            flash('Email does not exist', category='error')
            
    return render_template('singin.html', user=current_user)



@auth.route('/forgot_passoword', methods=['POST','GET'])
def change_pass():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        
        flash()
    
    return render_template("change_pass.html")