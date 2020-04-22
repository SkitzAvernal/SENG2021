from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from app import app, db, login
from flask_login import current_user, login_user, logout_user
from forms import SignUpForm, LoginForm
from webscraper import *
import random
import json
from models import User, Review, Bookmark, Event
from forms import SignUpForm, LoginForm, ReviewForm, PlannerForm
from sqlalchemy import desc
from datetime import datetime
import urllib.request
import urllib.parse
import json
from geopy import distance
from tsp_solver.greedy import solve_tsp


def get_distance(point1, point2):
    return distance.distance(point1, point2).km


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index(loginForm=None):
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
    plannerForm = PlannerForm()
    destinationList = []
    user_landmarks = []
    planner_bool = False
    startCoords = []
    path = []

    if plannerForm.validate_on_submit():
        planner_bool = True
        print(plannerForm.start.data)
        print(plannerForm.landmark1.data)
        print(plannerForm.landmark2.data)
        if plannerForm.landmark3.data:
            print(plannerForm.landmark3.data)
        if plannerForm.landmark4.data:
            print(plannerForm.landmark4.data)

        # get coordinates of landmark 1
        fetchURLstart = 'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=' + plannerForm.start.data + '&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
        fetchURLstart = fetchURLstart.replace(' ', '+')
        with urllib.request.urlopen(fetchURLstart) as response:
            data = json.loads(response.read().decode())
            result = data['Response']['View'][0]['Result'][0]
            startCoords = result['Location']['NavigationPosition'][0]
            startCoords = [startCoords['Latitude'], startCoords['Longitude']]
            startCategory = result['MatchLevel']
            startAddressLabel = result['Location']['Address']['Label']
            startAddressAditional = result['Location']['Address']['AdditionalData'][1]['value']
            # if len(data['Response']['View']) > 0 else None
        startDest = {"name": plannerForm.start.data, "latitude": startCoords[0], "longitude": startCoords[1]}
        destinationList.append(startDest)

        # get coordinates of landmark 1
        fetchURL1 = 'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=' + plannerForm.landmark1.data + '&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
        fetchURL1 = fetchURL1.replace(' ', '+')
        with urllib.request.urlopen(fetchURL1) as response:
            data = json.loads(response.read().decode())
            result = data['Response']['View'][0]['Result'][0]
            lm1Coords = result['Location']['NavigationPosition'][0]
            lm1Coords = [lm1Coords['Latitude'], lm1Coords['Longitude']]
            lm1Category = result['MatchLevel']
            lm1AddressLabel = result['Location']['Address']['Label']
            lm1AddressAditional = result['Location']['Address']['AdditionalData'][1]['value']
            # if len(data['Response']['View']) > 0 else None
        destination1 = {"name": plannerForm.landmark1.data, "latitude": lm1Coords[0], "longitude": lm1Coords[1]}
        destinationList.append(destination1)

        # get coordinates of landmark 2
        fetchURL2 = 'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=' + plannerForm.landmark2.data + '&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
        fetchURL2 = fetchURL2.replace(' ', '+')
        with urllib.request.urlopen(fetchURL2) as response:
            data = json.loads(response.read().decode())
            result = data['Response']['View'][0]['Result'][0]
            lm2Coords = result['Location']['NavigationPosition'][0]
            lm2Coords = [lm2Coords['Latitude'], lm2Coords['Longitude']]
            lm2Category = result['MatchLevel']
            lm2AddressLabel = result['Location']['Address']['Label']
            lm2AddressAditional = result['Location']['Address']['AdditionalData'][1]['value']
            # if len(data['Response']['View']) > 0 else None
        destination2 = {"name": plannerForm.landmark2.data, "latitude": lm2Coords[0], "longitude": lm2Coords[1]}
        destinationList.append(destination2)

        if plannerForm.landmark3.data:
            # get coordinates of landmark 3
            fetchURL3 = 'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=' + plannerForm.landmark3.data + '&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
            fetchURL3 = fetchURL3.replace(' ', '+')
            with urllib.request.urlopen(fetchURL3) as response:
                data = json.loads(response.read().decode())
                result = data['Response']['View'][0]['Result'][0]
                lm3Coords = result['Location']['NavigationPosition'][0]
                lm3Coords = [lm3Coords['Latitude'], lm3Coords['Longitude']]
                lm3Category = result['MatchLevel']
                lm3AddressLabel = result['Location']['Address']['Label']
                lm3AddressAditional = result['Location']['Address']['AdditionalData'][1]['value']
                # if len(data['Response']['View']) > 0 else None
            destination3 = {"name": plannerForm.landmark3.data, "latitude": lm3Coords[0], "longitude": lm3Coords[1]}
            destinationList.append(destination3)
        else:
            lm3Coords = None

        if plannerForm.landmark4.data:
            # get coordinates of landmark 4
            fetchURL4 = 'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext=' + plannerForm.landmark4.data + '&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
            fetchURL4 = fetchURL4.replace(' ', '+')
            with urllib.request.urlopen(fetchURL4) as response:
                data = json.loads(response.read().decode())
                result = data['Response']['View'][0]['Result'][0]
                lm4Coords = result['Location']['NavigationPosition'][0]
                lm4Coords = [lm4Coords['Latitude'], lm4Coords['Longitude']]
                lm4Category = result['MatchLevel']
                lm4AddressLabel = result['Location']['Address']['Label']
                lm4AddressAditional = result['Location']['Address']['AdditionalData'][1]['value']
                # if len(data['Response']['View']) > 0 else None
            destination4 = {"name": plannerForm.landmark4.data, "latitude": lm4Coords[0], "longitude": lm4Coords[1]}
            destinationList.append(destination4)
        else:
            lm4Coords = None

        print(startCoords)
        print(lm1Coords)
        print(lm2Coords)
        print(lm3Coords)
        print(lm4Coords)

        if lm3Coords != None and lm4Coords != None:
            fetch_url = f"https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={startCoords[0]},{startCoords[1]};{lm1Coords[0]},{lm1Coords[1]};{lm2Coords[0]},{lm2Coords[1]};{lm3Coords[0]},{lm3Coords[1]};{lm4Coords[0]},{lm4Coords[1]}&destinations={startCoords[0]},{startCoords[1]};{lm1Coords[0]},{lm1Coords[1]};{lm2Coords[0]},{lm2Coords[1]};{lm3Coords[0]},{lm3Coords[1]};{lm4Coords[0]},{lm4Coords[1]}&travelMode=driving&distanceUnit=km&key=AmiufPk0e3QV0l2SC-0A-XBgPH3rd6dCMmgyfyumfhh35u3BMjbY_4SXA70aOEtA"
            user_landmarks = [
                {
                    'coordinate': startCoords,
                    'name': plannerForm.start.data,
                    'index': 1,
                    'cost': None,
                    'category': startCategory,
                    'addressLabel': startAddressLabel,
                    'addressAdditional': startAddressAditional
                },
                {
                    'coordinate': lm1Coords,
                    'name': plannerForm.landmark1.data,
                    'index': 2,
                    'cost': None,
                    'category': lm1Category,
                    'addressLabel': lm1AddressLabel,
                    'addressAdditional': lm1AddressAditional
                },
                {
                    'coordinate': lm2Coords,
                    'name': plannerForm.landmark2.data,
                    'index': 3,
                    'cost': None,
                    'category': lm2Category,
                    'addressLabel': lm2AddressLabel,
                    'addressAdditional': lm2AddressAditional
                },
                {
                    'coordinate': lm3Coords,
                    'name': plannerForm.landmark3.data,
                    'index': 4,
                    'cost': None,
                    'category': lm3Category,
                    'addressLabel': lm3AddressLabel,
                    'addressAdditional': lm3AddressAditional
                },
                {
                    'coordinate': lm4Coords,
                    'name': plannerForm.landmark4.data,
                    'index': 5,
                    'cost': None,
                    'category': lm4Category,
                    'addressLabel': lm4AddressLabel,
                    'addressAdditional': lm4AddressAditional
                }
            ]
        elif lm3Coords != None:
            fetch_url = f"https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={startCoords[0]},{startCoords[1]};{lm1Coords[0]},{lm1Coords[1]};{lm2Coords[0]},{lm2Coords[1]};{lm3Coords[0]},{lm3Coords[1]}&destinations={startCoords[0]},{startCoords[1]};{lm1Coords[0]},{lm1Coords[1]};{lm2Coords[0]},{lm2Coords[1]};{lm3Coords[0]},{lm3Coords[1]}&travelMode=driving&distanceUnit=km&key=AmiufPk0e3QV0l2SC-0A-XBgPH3rd6dCMmgyfyumfhh35u3BMjbY_4SXA70aOEtA"
            user_landmarks = [
                {
                    'coordinate': startCoords,
                    'name': plannerForm.start.data,
                    'index': 1,
                    'cost': None,
                    'category': startCategory,
                    'addressLabel': startAddressLabel,
                    'addressAdditional': startAddressAditional
                },
                {
                    'coordinate': lm1Coords,
                    'name': plannerForm.landmark1.data,
                    'index': 2,
                    'cost': None,
                    'category': lm1Category,
                    'addressLabel': lm1AddressLabel,
                    'addressAdditional': lm1AddressAditional
                },
                {
                    'coordinate': lm2Coords,
                    'name': plannerForm.landmark2.data,
                    'index': 3,
                    'cost': None,
                    'category': lm2Category,
                    'addressLabel': lm2AddressLabel,
                    'addressAdditional': lm2AddressAditional
                },
                {
                    'coordinate': lm3Coords,
                    'name': plannerForm.landmark3.data,
                    'index': 4,
                    'cost': None,
                    'category': lm3Category,
                    'addressLabel': lm3AddressLabel,
                    'addressAdditional': lm3AddressAditional
                }
            ]
        else:
            fetch_url = f"https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins={startCoords[0]},{startCoords[1]};{lm1Coords[0]},{lm1Coords[1]};{lm2Coords[0]},{lm2Coords[1]}&destinations={startCoords[0]},{startCoords[1]};{lm1Coords[0]},{lm1Coords[1]};{lm2Coords[0]},{lm2Coords[1]}&travelMode=driving&distanceUnit=km&key=AmiufPk0e3QV0l2SC-0A-XBgPH3rd6dCMmgyfyumfhh35u3BMjbY_4SXA70aOEtA"
            print(fetch_url)
            user_landmarks = [
                {
                    'coordinate': startCoords,
                    'name': plannerForm.start.data,
                    'index': 1,
                    'cost': None,
                    'category': startCategory,
                    'addressLabel': startAddressLabel,
                    'addressAdditional': startAddressAditional
                },
                {
                    'coordinate': lm1Coords,
                    'name': plannerForm.landmark1.data,
                    'index': 2,
                    'cost': None,
                    'category': lm1Category,
                    'addressLabel': lm1AddressLabel,
                    'addressAdditional': lm1AddressAditional
                },
                {
                    'coordinate': lm2Coords,
                    'name': plannerForm.landmark2.data,
                    'index': 3,
                    'cost': None,
                    'category': lm2Category,
                    'addressLabel': lm2AddressLabel,
                    'addressAdditional': lm2AddressAditional
                }
            ]
        response = requests.get(fetch_url)
        data = response.json()
        destinations = data['resourceSets'][0]['resources'][0]['destinations']
        distance_matrix = data['resourceSets'][0]['resources'][0]['results']
        n = len(destinations)
        matrix = []
        i = 0
        j = 0
        while i < n:
            append_matrix = []
            j = 0
            while j < n:
                append_matrix.append(0)
                j += 1
            i += 1
            matrix.append(append_matrix)

        for item in distance_matrix:
            if item['originIndex'] == 0 and item['destinationIndex'] == 0:
                matrix[0][0] = 0
            else:
                matrix[int(item['originIndex'])][int(item['destinationIndex'])] = item['travelDistance']

        print(matrix)

        # This code block is taken from taken from https://github.com/abhishekjiitr/tsp-python/blob/master/helper.py
        # With some modification

        from math import isinf, sqrt, degrees, acos

        def in_subset(i, s):
            while i > 0 and s > 0:
                s = s >> 1
                i -= 1
            cond = s & 1
            return cond

        def remove(i, s):
            x = 1
            x = x << i
            l = length(s)
            l = 2 ** l - 1
            x = x ^ l
            return x & s

        def get_path(p):
            n = len(p[0])
            number = 2 ** n - 2
            prev = p[number][0]
            path = []
            while prev != -1:
                path.append(prev)
                number = remove(prev, number)
                prev = p[number][prev]
            reversepath = [str(path[len(path)-i-1]+1) for i in range(len(path))]
            reversepath.append("1")
            reversepath.insert(0, "1")
            return reversepath

        def generate_subsets(n):
            l = []
            for i in range(2**n):
                l.append(i)
            return sorted(l, key = lambda x : size(x) )

        def make_graph(n):
            a = [ [-1 for i in range(n)] for j in range(n)]
            for i in range(n):
                for j in range(n):
                    rand = randint(0, n)
                    if a[i][j] < 0:
                        a[i][j] = rand
                        a[j][i] = rand
                    if i == j:
                        a[i][i] = 0
            return a
        def size(int_type):
            length = 0
            count = 0
            while (int_type):
                count += (int_type & 1)
                length += 1
                int_type >>= 1
            return count

        def length(int_type):
            length = 0
            count = 0
            while (int_type):
                count += (int_type & 1)
                length += 1
                int_type >>= 1
            return length

        def tsp(a):
            n = len(a)
            l = generate_subsets(n)
            cost = [ [-1 for city in range(n)] for subset in l]
            p = [ [-1 for city in range(n)] for subset in l]

            count = 1
            total = len(l)
            for subset in l:
                for dest in range(n):
                    if not size(subset):
                        cost[subset][dest] = a[0][dest]
                        print (dest, subset)
                    elif (not in_subset(0, subset)) and (not in_subset(dest, subset)) :
                        mini = float("inf")
                        for i in range(n):
                            if in_subset(i, subset):
                                modifiedSubset = remove(i, subset)
                                val = a[i][dest] + cost[modifiedSubset][i]

                                if val < mini:
                                    mini = val
                                    p[subset][dest] = i

                        if not isinf(mini):
                            cost[subset][dest] = mini
                count += 1
            path = get_path(p)

            Cost = cost[2**n-2][0]
            print("Total cost for travelling with minimum route is :",Cost)
            return path

        path = tsp(matrix)
        print(path)


    if current_user.is_authenticated:
        bookmarks = Bookmark.query.filter_by(username=current_user.username).order_by(Bookmark.landmark).all()
        events=Event.query.filter_by(username=current_user.username).all()
        return render_template('index.html',
                               lon=lon,
                               lat=lat,
                               zoom=zoom,
                               loginForm=loginForm,
                               bookmarks=bookmarks,
                               plannerForm=plannerForm,
                               destinationList=destinationList,
                               trip_planner=user_landmarks,
                               planner=planner_bool,
                               planner_origin=startCoords,
                               path = path,
                               events = events)

    return render_template('index.html',

                           lon=lon,
                           lat=lat,
                           zoom=zoom,
                           loginForm=loginForm,
                           plannerForm=plannerForm,
                           destinationList=destinationList,
                           trip_planner=user_landmarks,
                           planner=planner_bool,
                           planner_origin=startCoords,
                           path = path)


@app.route('/index/postmethod', methods=['POST'])
@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.get_json()
    match_level = jsdata['jsdata']['match_level']
    landmark = jsdata['jsdata']['landmark']

    ###################### fetch landmark coordinate #######################################
    # fetch_url =  f'https://geocoder.ls.hereapi.com/6.2/geocode.json?searchtext={landmark}&gen=9&apiKey=PaSJdAi4_bn3hAFxrLoc_eVxEr74-hDTjGXhRICkhYs'
    # response = requests.get(fetch_url)
    # data = response.json()
    # coordinate = result['Location']['DisplayPosition']
    # latitude = coordinate['Latitude']
    # longitude = coordinate['Longitude']
    # match_level = result['MatchLevel']
    # state = result['Location']['Address']['AdditionalData'][1]['value']
    # address = result['Location']['Address']['Label']

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
    #     match_level = result['MatchLevel']
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
    print(res_dict)
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


    print('category is:', category)

    # get reviews
    reviewForm = ReviewForm()
    reviews = Review.query.filter_by(landmark=news_name).order_by(desc(Review.timestamp)).all()
    # print(reviews)
    return render_template('landmark.html',
                           name=news_name,
                           image=info_scraper.get_image(),
                           desc=info_scraper.get_description(),
                           events=events_scraper.get_events(),
                           news_name=news_name,
                           category=category,
                           reviewForm=reviewForm,
                           reviews=reviews)
# @app.route('/landmark/<lm_name>')
# def landmark(lm_name):
#     reviewForm = ReviewForm()
#     reviews = Review.query.filter_by(landmark=lm_name).order_by(desc(Review.timestamp)).all()
#     # print(reviews)
#     return render_template('landmark.html', name = lm_name, reviewForm=reviewForm, reviews=reviews)


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
        return redirect(url_for('index'))

    if loginForm.validate_on_submit():
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index', loginForm=loginForm))
        login_user(user)
        return redirect(url_for('index'))

    return redirect(url_for('index'))


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
    landmark = request.form.get('landmark')
    category = request.form.get('category')
    exists = db.session.query(Bookmark.landmark).filter_by(username=current_user.username).scalar()
    if exists is not None:
        return redirect(request.referrer)
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


@app.route('/events', methods=['POST'])
def events():
    if not current_user.is_authenticated:
        return redirect(request.referrer)
    name = request.form.get('name')
    date = request.form.get('date')
    url = request.form.get('url')
    print(name)

    exists = db.session.query(Event.name).filter_by(username=current_user.username, url=url).scalar()
    if exists is not None:
        return redirect(request.referrer)

    event = Event(username=current_user.username, name=name, date=date, url=url)
    db.session.add(event)
    db.session.commit()

    return redirect(request.referrer)

@app.route('/rm_event', methods=['POST'])
def rm_event():
    if not current_user.is_authenticated:
        return redirect(request.referrer)

    name = request.form.get('event')
    event = Event.query.filter_by(username=current_user.username, name=name).first()
    db.session.delete(event)
    db.session.commit()
    return redirect(request.referrer)
