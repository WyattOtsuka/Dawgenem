from flask import Flask, render_template, send_from_directory, request, session
import json
import pandas as pd
import get_info
from pyrate_limiter import Duration, RequestRate, Limiter, BucketFullException


app = Flask(__name__)

per_second_rate = RequestRate(19, Duration.SECOND) # 20 requests per second
minute_rate = RequestRate(99, Duration.MINUTE * 2) # 100 requests per 2 minutes
limiter = Limiter(per_second_rate, minute_rate)

@app.route("/")
@app.route("/home")
@app.route("/home/<data>")
def hello_world(data=None):
    #if data == None:
        return render_template('home.html', score = "66")
        
    #else:
    #   return render_template('home.html', input = data)
@app.route("/updateLog")
def updateLog():
    return render_template('updateLog.html')

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
    
@app.route('/about')
def testing_page_entry():
    return render_template('about.html')
    
@app.route('/submit')
def submit():
    req = request.form
    print(req)
    return render_template('test_entry.html')

@app.route('/privacy')
def privacy():
        return render_template('privacy.html')


@app.route('/search')
def search():
    username = request.args.get('username')
    if username != "":
        print (f"Search: Valid username passed in, {username}")
        results = get_info.get_score(username, limiter)
        return "Overall score:\t{},Moon score:\t{},Dog Cat score:\t{},KDA score:\t\t{}".format(results[0], results[1], results[2], results[3])
    else:
        print("Search: Empty Username")
        return 