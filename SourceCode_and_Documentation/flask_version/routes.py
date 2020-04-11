from flask import Flask, render_template, request, redirect, url_for, flash 
from app import app, db, login 
from flask_login import current_user, login_user, logout_user 
from models import User, Review 
from forms import SignUpForm, LoginForm, ReviewForm
from sqlalchemy import desc
from datetime import datetime

@app.route('/')
@app.route('/index/')
def index():
    lon = 16832505.12095191

    lat = -4011613.961964385
    zoom = 12
    if request.args.get('lon'):
        lon = float(request.args.get('lon'))
    if request.args.get('lat'):
        lat = float(request.args.get('lat'))
    if request.args.get('zoom'):
        zoom = float(request.args.get('zoom'))

    loginForm = LoginForm()
    return render_template('index.html',
                           lon = lon,
                           lat = lat,
                           zoom = zoom, 
                           loginForm = loginForm)

@app.route('/landmark/<lm_name>')
def landmark(lm_name):
    reviewForm = ReviewForm()
    reviews = Review.query.filter_by(landmark=lm_name).order_by(desc(Review.timestamp)).all()
    # print(reviews)
    return render_template('landmark.html', name = lm_name, reviewForm=reviewForm, reviews=reviews)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupForm = SignUpForm()
    loginForm = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if signupForm.validate_on_submit():
        user = User(username=signupForm.username.data, email=signupForm.email.data)
        user.set_password(signupForm.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', signupForm=signupForm)

@app.route('/login', methods=['POST'])
def login():
    loginForm = LoginForm()

    if current_user.is_authenticated:
        return render_template('index.html', loginForm=loginForm)

    if loginForm.validate_on_submit():
        user = User.query.filter_by(username=loginForm.username.data).first() 
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid username or password')
            return render_template('index.html', loginForm=loginForm)
        login_user(user)
        return redirect(url_for('index'))

    return render_template('index.html', loginForm=LoginForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/review', methods=['POST'])
def review():
    reviewForm = ReviewForm()

    if not current_user.is_authenticated:
        return redirect(request.referrer)

    if reviewForm.validate_on_submit():
        landmark = request.form.get('landmark_name')
        rating = request.form['rating']
        print('rating is', rating)
        # print('body', reviewForm.body.data)
        # print('username', current_user.username)
        # print('landmark', landmark)
        review = Review(body=reviewForm.body.data, username=current_user.username, landmark=landmark, timestamp=datetime.now(), rating=rating)
        db.session.add(review)
        db.session.commit()
        return redirect(request.referrer)

    return render_template(request.referrer)