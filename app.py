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

@app.route("/for_load_img",methods =['POST'])
def for_load_img():
    
    file = request.files['file'] 

    if file:
        
        _ ,fileextension = os.path.splitext(file.filename)
        filename =  session["name"] + fileextension
        filepath = os.path.join('static/img', filename)
        file.save(filepath)
        global gray_filepath, histogram_filepath
        gray_filepath = aip.img_to_gray(filepath,filename)
        histogram_filepath = aip.img_to_histogram(gray_filepath, filename)
        gaussion_noise_filepath = aip.img_to_gaussion_noise(gray_filepath, filename)
        haar_wavelet_filepath = aip.img_to_haar_wavelet(gray_filepath, filename)
        histogram_equalization_filepath = aip.img_to_histogram_equalization(gray_filepath, filename)
        global response
        response = jsonify(gray=gray_filepath[6:] ,histogram = histogram_filepath[6:] \
            ,gaussion_noise = gaussion_noise_filepath[6:] , haar_wavelet = haar_wavelet_filepath[6:]\
            ,histogram_equalization = histogram_equalization_filepath[6:])
        return response
    else:
        return jsonify(success=False)

@app.route("/for_load_aip_img",methods=['POST'])
def for_load_aip_img():
    #file = request.form.get('updatetype')
    return response

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
    #處理db
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

    print(password)
    
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

