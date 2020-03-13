from flask import Flask, render_template, request



app = Flask(__name__, static_url_path='/static')

@app.route('/')
@app.route('/index')
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
    return render_template('index.html',
                           lon = lon,
                           lat = lat,
                           zoom = zoom)


@app.route('/landmark')
def landmark():
    return render_template('landmark.html')




if __name__ == '__main__':
    app.run(debug = True, port = 5000)