"""
Flask with regression

"""

import datetime
import pickle
import json
from flask.helpers import url_for
from flask_wtf.recaptcha import validators
import pandas as pd
import numpy as np
from sklearn import preprocessing
from flask import Flask, render_template,redirect
from flask import request
from flask_login import LoginManager,logout_user,login_user,login_required
from functions import array_to_df, testpre_processing
from dbmodel import User, create_db, get_user, register_user
from appconfig import app,db,file_name
from forms import LoginForm,RegisterForm



# from appconfig import app, db, file_name
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


create_db(file_name)

model = pickle.load(open('model.pkl', 'rb'))

#app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/account")
@login_required 
def account():
    return "account"

@app.route("/settings")
def settings():
    return "settings"

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username_posted =form.username.data
        password_posted = form.password.data
        
        user1 = get_user(username_posted,password_posted)
        if user1:
            print("__________ user found.")
            login_user(user1)
            return redirect(url_for("hesapla"))

    return render_template("login.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        register_user(username,email,password)
        return redirect(url_for("index"))
    return render_template("register.html",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/hesapla", methods=['GET', 'POST'])
@login_required 
def hesapla():
    if request.method == 'POST':
        # Post edilmiş bir veri var
        if request.form.get("cancel")=="return":

            return redirect(url_for("index"))

        elif request.form.get("submit") == "submitted" :

            bedrooms = request.form["bedrooms"]
            bathrooms = request.form["bathrooms"]
            area_living = request.form["area_living"]
            area_lot = request.form["area_lot"]
            floors = request.form["floors"]
            waterfront = request.form["waterfront"]
            view = request.form["view"]
            condition = request.form["condition"]
            area_above = request.form["area_above"]
            area_basement = request.form["area_basement"]
            built = request.form["built"]
            renovated =request.form["renovated"]
            city = request.form["city"]
            zip = request.form["zip"]
            country = request.form["country"]
            list1 = [bedrooms, bathrooms, area_living, area_lot, floors, waterfront,
                                view, condition, area_above, area_basement, built, renovated, city, zip, country]
            final_features = array_to_df(list1)
            final_features.to_json("request.json", orient="index")
            final_features = testpre_processing(final_features)
            y_pred = model.predict(final_features)
            
    else:
        # post değil,demek ki GET
        bedrooms = None
        bathrooms = None
        area_living = None
        area_lot = None
        floors = None
        waterfront = None
        view = None
        condition = None
        area_above = None
        area_basement = None
        built = None
        city = None
        zip = None
        country = None
        y_pred = None
        final_features = None
        list1 = None
    
    return render_template("hesapla.html",df1=y_pred)
    

    # PREDİCT : 373186.96134434
    # REAL :     342000.0




@app.route("/api/time", methods=["GET"])
def api_time():
    """
    parametre almayan, JSON donduren bir API örneği.
    requires :
        import datetime
    """
    now = datetime.datetime.now()
    dnow = {}
    dnow["now"] = now
    
    return dnow  
    # return str(now) # dict olmadığı için str döndü.


@app.route("/api/price/<int:bedrooms>/<int:bathrooms>/<string:city>")
def api_price(bedrooms, bathrooms, city):
    """
    Bu fonksiyonun özelliği dışardan alabilir vaziyette. Değerleri URL
    üzerinden alıyor.
    curl -v http://127.0.0.1:5000/api/price/2/3/new%20york

    """
    
    price = bedrooms*bathrooms*100000
    print(bedrooms, bathrooms, city)
    
    dprice = {"price": price}
    return dprice


@app.route("/api/degerle2/", methods=["POST", "GET"])
def degerle2():
    
    """
    requires:
        from flask import request
    """
    if request.json:

        # request, json format
         data = request.json
         print(data)
         df=pd.DataFrame(data["0"],index=[0])
         df= testpre_processing(df)
         y_pred = model.predict(df)
         print(y_pred[0])
         return json.dumps({"price":y_pred[0]}) 
        # raise ValueError("data is not JSON.")
    else:
        
        return {"ERROR": "JSON expected"}
