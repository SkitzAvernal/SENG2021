from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from app import app, db, login 
from flask_login import current_user, login_user, logout_user 
from webscraper import *
import random, json
from models import User, Review, Bookmark
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
    
    if current_user.is_authenticated:
        bookmarks = Bookmark.query.filter_by(username=current_user.username).order_by(Bookmark.landmark).all()
        return render_template('index.html', 
				        	lon = lon, 
				        	lat = lat, 
				        	zoom = zoom, 
				        	loginForm = loginForm,
				        	bookmarks=bookmarks)

    return render_template('index.html',
                           lon = lon,
                           lat = lat,
                           zoom = zoom, 
                           loginForm = loginForm)


@app.route('/index/postmethod', methods = ['POST'])
@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.get_json()
    match_level = jsdata['jsdata']['match_level']
    landmark = jsdata['jsdata']['landmark']

    ###################### fetch landmark coordinate ####################################### 
    # fetch_url =  f'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext={landmark}&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
    # response = requests.get(fetch_url)
    # data = response.json()
    # coordinate = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
    # latitude = coordinate['Latitude']
    # longitude = coordinate['Longitude']
    # match_level = data['Response']['View'][0]['Result'][0]['MatchLevel']
    # state = data['Response']['View'][0]['Result'][0]['Location']['Address']['AdditionalData'][1]['value']
    # address = data['Response']['View'][0]['Result'][0]['Location']['Address']['Label']
    
    ###################### fetch landmark description using webscraper #####################
    search_name = landmark
    if match_level == "city":
        search_name = landmark.split(',')[0]
    events_scraper = Events_scraper(search_name)   
    info_scraper = Info_scraper(landmark)
    img_src = info_scraper.get_image()
    # description = info_scraper.get_description()

    res_dict = {
        # 'landmark': landmark,
        # 'match_level': match_level,
        # 'latitude': int(latitude),
        # 'longitude': int(longitude),
        # 'address': address,
        'image': img_src
        # 'description': description
    }
    # result = {
    #     'lm_data': res_dict
    # }


    ##################### fetch landmarks near landmark ####################################
    # nearby = []
    # fetch_url = f'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=4ZRwHTCnCEe1HV3smhin6xJBjTP9r8zwWyZz-8rM3a4&mode=retrieveLandmarks&prox={latitude},{longitude},100000'
    # response = requests.get(fetch_url)
    # data = response.json()
    # i = 0
    # for result in data['Response']['View'][0]['Result']:
    #     if result['Location']['Address'].__contains__('District'):
    #         city = result['Location']['Address']['District']
    #     else:
    #         city = result['Location']['Address']['City']
    #     landmark = result['Location']['Name']
    #     match_level = data['Response']['View'][0]['Result'][0]['MatchLevel']
    #     latitude = result['Location']['DisplayPosition']['Latitude']
    #     longitude = result['Location']['DisplayPosition']['Longitude']
    #     address = result['Location']['Address']['Label']

    #     ##################### fetch nearby landmark info using web scraper ######################

    #     search_name = landmark
    #     if match_level == "city":
    #         search_name = landmark.split(',')[0]
    #     events_scraper = Events_scraper(search_name)   
    #     info_scraper = Info_scraper(landmark)
    #     img_src = info_scraper.get_image()
    #     # description = info_scraper.get_description()

    #     res_dict = {
    #         'city': city,
    #         'landmark': landmark,
    #         'match_level': match_level,
    #         'latitude': int(latitude),
    #         'longitude': int(longitude),
    #         'address': address,
    #         'image': img_src
    #         # 'description': description
    #     }
    #     nearby.append(res_dict)
    #     if i >= 2:
    #         break
    #     i += 1

    # result.update({
    #     'nearby': nearby
    # })
    print (res_dict)
    return jsonify(res_dict)
	

@app.route('/landmark/<category>/<lm_name>')
def landmark(category, lm_name):
    # use the web scraper here
    search_name = lm_name
    news_name = lm_name.split(',')[0]
    if category == "city":
        search_name = lm_name.split(',')[0]
    events_scraper = Events_scraper(search_name)   
    info_scraper = Info_scraper(lm_name)
    reviewForm = ReviewForm()
    reviews = Review.query.filter_by(landmark=lm_name).order_by(desc(Review.timestamp)).all()
    return render_template('landmark.html', 
                            name = search_name, 
                            image = info_scraper.get_image(), 
                            desc = info_scraper.get_description(), 
                            events = events_scraper.get_events(), 
                            news_name = news_name, 
                            reviewForm = reviewForm, 
                            reviews = reviews,
                            category = category)


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


@app.route('/bookmark', methods=['POST'])
def bookmark():
    if not current_user.is_authenticated:
        return redirect(request.referrer)
    postData = request.form
    landmark = postData['landmark']
    category = postData['category']

    #category = request.form['category']
    #print(request.form['category'])
    print('hi')
    print('user is {} nd landmark is{} and category is {}'.format(current_user.username, landmark, category))
    bookmark = Bookmark(username=current_user.username, landmark=landmark, category=category)
    db.session.add(bookmark)
    db.session.commit()

    return redirect(request.referrer)

@app.route('/rm_bookmark', methods=['POST'])
def rm_bookmark():
    if not current_user.is_authenticated:
        return redirect(request.referrer)

    landmark = request.form['landmark']
    #print('user is {} nd landmark is{}'.format(current_user.username, landmark))
    bookmark = Bookmark.query.filter_by(username=current_user.username, landmark=landmark).first()
   # print(bookmark)
    db.session.delete(bookmark)
    db.session.commit()
    return redirect(request.referrer)