from flask import *
from pymongo import MongoClient
import json
from flask_assets import Environment, Bundle
import os
import aip
from flask_cors import CORS
import bcrypt
import hashlib
import base64
import numpy as np


client = MongoClient("mongodb+srv://root:root123@atlascluster.uu7phqt.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster")
db = client.mywebsite #選db

app = Flask(
    __name__,
    #static file的folder和url
    static_folder="static", #對應的資料夾名稱
    static_url_path="/" #如果修改static為abc，則url就是abc
)
CORS(app)
app.secret_key="any string but secret"

@app.route("/") #註冊帳號頁面
def index():
    return render_template("signup.html")

@app.route("/login") #登入帳號頁面
def login():
    error_message = None
    return render_template("login.html")


@app.route("/my_cv") #cv頁面
def my_cv():
    if "name" in session:
        print("@@@@@@@@@@@@@@")
        print(session)
        print("@@@@@@@@@@@@@@")
        return render_template("my_cv.html")
    else:
        return redirect("/login")

@app.route("/my_aip",methods = ["GET","POST"]) 
def my_aip():
    if "name" in session:
        return render_template("my_aip.html")
    else:
        return redirect("/login")

@app.route("/for_load_img",methods =['POST']) #處理輸入照片
def for_load_img():
    file = request.files['file']
    if file:
        npimg = np.frombuffer(file.read(), np.uint8)
        gray_img = aip.img_to_gray(npimg) #照片
        result = db.users_createphoto.find_one({"name" : session["name"]})
        if result is None: 
            db.users_createphoto.insert_one({
                "name" : session["name"],
                "gray_img" : gray_img})
        else:
            db.users_createphoto.update_one(
                {"name" : session["name"]},     # 查找條件
                {"$set": {"gray_img": gray_img }})  # 更新操作
        return jsonify({"gray_img": gray_img})
    else:
        return jsonify(success=False)

@app.route("/for_load_aip_img",methods=['POST'])
def for_load_aip_img():
    updatetype = request.form.get('updatetype') #選處理方式
    img = db.users_createphoto.find_one({"name" : session["name"]})
    if img is not None:
        gray_img = img.get("gray_img")
        if updatetype == "histogram":
            update_img = aip.img_to_histogram(gray_img)
            print("AAAAAAAAAAAAAAAA")
        elif updatetype == "gaussion_noise":
            update_img = aip.img_to_gaussion_noise(gray_img)
        elif updatetype == "haar_wavelet":
            update_img = aip.img_to_haar_wavelet(gray_img)
        elif updatetype == "histogram_equalization":
            update_img = aip.img_to_histogram_equalization(gray_img)
            
        db.users_createphoto.update_one(
            {"name": session["name"]},           # 查找條件
            {"$set": { updatetype : update_img}})  # 使用 $push 新增資料到 photo 欄位
        print("BBBBBBBBBBBBBBBB")
        return jsonify({updatetype : update_img})
    return jsonify(success = False)


    
@app.route("/member") #首頁
def member():
    if "name" in session:
        return render_template("member.html")
    else:
        return redirect("/login")

@app.route("/for_signup",methods=["POST"]) #處理註冊
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]
    #加密密碼
    salt = hashlib.sha256(email.encode('utf-8')).digest()
    salt = base64.b64encode(salt).decode('utf-8')

    # 將Base64字串中的+/替換為bcrypt允許的字符，並截斷至22字符長度
    salt = salt.replace('+', '.').replace('/', '.')[:22]
    salt = f"$2b$12${salt}"
    password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))  # 雜湊密碼
    collection = db.users
    result = collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?message=信箱被註冊過了～")
    else:
        collection.insert_one({
            "name": name,
            "email":email,
            "password":password,
            "phone":phone
        })
        return redirect("/login")

@app.route("/for_signin",methods=["POST"]) #處理登入
def signin():
    email = request.form['username']  # 獲取用戶輸入的帳號
    password = request.form['password']  # 獲取用戶輸入的密碼
    
    #加密密碼
    salt = hashlib.sha256(email.encode('utf-8')).digest()
    salt = base64.b64encode(salt).decode('utf-8')

    # 將Base64字串中的+/替換為bcrypt允許的字符，並截斷至22字符長度
    salt = salt.replace('+', '.').replace('/', '.')[:22]
    salt = f"$2b$12${salt}"
    password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))  # 雜湊密碼
    collection = db.users #使用user database
    result = collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}]
    })
    #看是否有找到會員資料
    if result != None:
        session["name"] = result["name"]
        return redirect("/my_cv")
    return render_template('login.html', error_message="帳號密碼錯誤")

@app.route("/error") #錯誤訊息回傳
def error():
    message = request.args.get("msg" , "發生錯誤")
    return render_template("error.html",message = message)

@app.route("/for_signout")
def signout():
    if session["name"]:
        del session["name"]
    return redirect("/login")

@app.route("/signup")
def for_signup():
    return render_template("signup.html")

@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/for_forgot_password",methods=["POST"])
def get_password():
    email = request.form["email"]
    phone = request.form["phone"]
    collection = db.users #使用user database
    result = collection.find_one({
        "$and":[
            {"email":email},
            {"phone":phone}]
    })
    print(result)
    if result != None:
        return render_template('forgot_password.html', password_message="password is : "+ result["password"])
    else:
        return render_template('forgot_password.html', password_message="不存在帳號或電話")
    #return render_template("login.html")
app.run(port=3000)

