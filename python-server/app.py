# installed
# ========================================
from flask import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_mongoengine import MongoEngine
from flask_qrcode import QRcode
from werkzeug.urls import url_parse
import pymongo

import hashlib 

from colorama import init, Fore, Back, Style
init()
# ========================================

# built-in
# ========================================
import os
import re
from datetime import datetime
from typing import Collection
from pprint import pprint
import base64
import traceback
# ========================================

# custom
# ========================================
from form import LoginForm, PasswordChangeForm
from cims_report import *
from cims_email import *
# ========================================



def cprint(color,obj):
    colors = {"r": Fore.RED,
              "b": Fore.BLUE,
              "g": Fore.GREEN,
              "w": Fore.WHITE,           
            }
    try:
        print(colors[color],obj,Fore.RESET)
    except:
        print(obj)

CIMS_DOMAIN      = os.environ["CIMS_DOMAIN"]
CIMS_DATABASE    = os.environ["CIMS_DATABASE"]
CIMS_COLLECTION  = os.environ["CIMS_COLLECTION"]
CIMS_MONGOUSER   = os.environ["CIMS_MONGOUSER"]
CIMS_MONGOPASSWD = os.environ["CIMS_MONGOPASSWD"]
CIMS_MONGOIP     = os.environ["CIMS_MONGOIP"]
FLASK_SEC_KEY    = os.environ["FLASK_SEC_KEY"]

app = Flask(__name__, template_folder='templates')
qrcode = QRcode(app)

# ==================================================================
#                           MongoDB Setup
# ==================================================================
app.config['MONGODB_SETTINGS'] = {
    'db'  : CIMS_DATABASE,
    'host': CIMS_MONGOIP,
    'port': 27017,
    'username' : CIMS_MONGOUSER,
    'password' : CIMS_MONGOPASSWD,
    'authentication_source': 'admin'
}
app.secret_key = FLASK_SEC_KEY

db = MongoEngine(app)

login  = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

class User(UserMixin, db.Document):
    meta = {"collection":"users"}
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()

myclient = pymongo.MongoClient(
    "mongodb://{}:27017/".format(CIMS_DOMAIN), 
    username = CIMS_MONGOUSER,
    password = CIMS_MONGOPASSWD
)

mydb = myclient[CIMS_DATABASE]
mycoll = mydb[CIMS_COLLECTION]
# ==================================================================

@app.route('/favicon')
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'prl.png', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET',"POST"])
@app.route('/login', methods=['GET',"POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("form"))
    
    form = LoginForm()

    if form.validate_on_submit():
        # cprint("r",form.username.data)
        # cprint("r",form.password.data)
        
        password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = User.objects(username=form.username.data,password=password_hash).first()

        if user is None:# or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        
        login_user(user,remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('form')
            
        return redirect(next_page)
    
    else:
        return render_template('login.html', form=form)


@app.route('/form', methods=['GET',"POST"])
@login_required
def form():

    try:
        # cpu_list = list(mydb['ram'].find({},{"brand":True, "_id": False}))
        cpu_list         = sorted(list(mydb['cpu'].distinct("brand")))
        ram_list         = sorted(list(mydb['ram'].distinct("brand")))
        motherboard_list = sorted(list(mydb['motherboard'].distinct("brand")))
        harddisk_list    = sorted(list(mydb['harddisk'].distinct("brand")))
        smps_list        = sorted(list(mydb['smps'].distinct("brand")))
        cabinet_list     = sorted(list(mydb['cabinet'].distinct("brand")))
        monitor_list     = sorted(list(mydb['monitor'].distinct("brand")))
        mouse_list       = sorted(list(mydb['mouse'].distinct("brand")))
        keyboard_list    = sorted(list(mydb['keyboard'].distinct("brand")))
        speakers_list    = sorted(list(mydb['speakers'].distinct("brand")))
        webcam_list      = sorted(list(mydb['webcam'].distinct("brand")))
        

    except Exception as e:
        status_code = Response(status=400)
        return status_code

    return render_template("form.html", 
                            cpu_list = cpu_list,
                            ram_list = ram_list,
                            motherboard_list = motherboard_list,
                            harddisk_list = harddisk_list,
                            smps_list = smps_list,
                            cabinet_list = cabinet_list,
                            monitor_list = monitor_list,
                            mouse_list = mouse_list,
                            keyboard_list =  keyboard_list, 
                            speakers_list =  speakers_list, 
                            webcam_list =  webcam_list 
                            )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/view_data',methods=["GET","POST"])
@login_required
def view_data():
    cpu_list         = sorted(list(mydb['cpu'].distinct("brand")))
    ram_list         = sorted(list(mydb['ram'].distinct("brand")))
    motherboard_list = sorted(list(mydb['motherboard'].distinct("brand")))
    harddisk_list    = sorted(list(mydb['harddisk'].distinct("brand")))
    smps_list        = sorted(list(mydb['smps'].distinct("brand")))
    cabinet_list     = sorted(list(mydb['cabinet'].distinct("brand")))
    monitor_list     = sorted(list(mydb['monitor'].distinct("brand")))
    mouse_list       = sorted(list(mydb['mouse'].distinct("brand")))
    keyboard_list    = sorted(list(mydb['keyboard'].distinct("brand")))
    speakers_list    = sorted(list(mydb['speakers'].distinct("brand")))
    webcam_list      = sorted(list(mydb['webcam'].distinct("brand")))


    return render_template("view_data.html", 
                        cpu_list = cpu_list,
                        ram_list = ram_list,
                        motherboard_list = motherboard_list,
                        harddisk_list = harddisk_list,
                        smps_list = smps_list,
                        cabinet_list = cabinet_list,
                        monitor_list = monitor_list,
                        mouse_list = mouse_list,
                        keyboard_list =  keyboard_list, 
                        speakers_list =  speakers_list, 
                        webcam_list =  webcam_list 
                        )

@app.route('/search_data',methods=["POST"])
@login_required
def search_data():
    json = request.json
    
    data = mycoll.find_one({"_id": json["pcdt-id"] })
    
    if data:
        data["type"] = "msg"
        return jsonify(data)

    else:
        return jsonify({
            "msg":f"PCDT-ID {json['pcdt-id']} <br> No Record Found!",
            "type":"msg"
            }),404

@app.route('/change_password',methods=["GET","POST"])
@login_required
def change_password():

    form = PasswordChangeForm()

    if form.validate_on_submit():
        mydb['users'].update_one(
            {"username":current_user.username},
            {"$set" :{
                "password": hashlib.sha256(form.new_password.data.encode()).hexdigest()}}
            )
        return redirect(url_for("logout"))
        
    else:
        return render_template("change_password.html", form=form)

@app.route('/add_data', methods=["POST"])
@login_required
def add_data():
    record = request.json
    pprint(record)

    result = {}

    for key in record.keys():
        if isinstance(record[key], list) and not record[key][1].strip():
            result[key] = "Empty"
        elif isinstance(record[key], str) and not record[key].strip():
            result[key] = "Empty"

    if bool(result):
        result["msg"] = "Fill the Red Highlighted Fields!"
        return jsonify(result), 400

    #================================================================== 
    #  Regex Pay Roll Check
    #================================================================== 
    payroll = re.compile("^PR\d{5}")
    
    record["custodian-payroll"] = record["custodian-payroll"].upper()

    if not bool(payroll.match(record["custodian-payroll"])):
        result["custodian-payroll"] = "Empty"
        result["msg"] = "Pay Roll Number is Not in Correct Format!"
        return jsonify(result), 400
    #==================================================================

    #================================================================== 
    #  Regex PO Number Check
    #================================================================== 
    ponumber = re.compile("^\d{14}|\d{4}E\d{9}")

    record["coins-po-number"] = record["coins-po-number"].upper()
    record["gem-po-number"] = record["gem-po-number"].upper()
    
    if not bool(ponumber.match(record["coins-po-number"])):
        result["coins-po-number"] = "Empty"
        result["msg"] = "Coins PO Number is Not in Correct Format!"
        return jsonify(result), 400
    #==================================================================

    primary_key = datetime.now().strftime("%Y%m%d%f")
    record["_id"] = primary_key

    warranties = list(mydb["warranty"].find({},{"_id":0,"part":1, "period":1}))    
    warranties = dict(
        zip( [doc["part"] for doc in warranties] ,
        [doc["period"] for doc in warranties])
    )

    record["cpu"].append(warranties["cpu"])
    record["motherboard"].append(warranties["motherboard"])
    record["ram"].append(warranties["ram"])
    record["hdd"].append(warranties["hdd"])
    record["ssd"].append(warranties["ssd"])
    record["smps"].append(warranties["smps"])
    record["cabinet"].append(warranties["cabinet"])
    record["monitor"].append(warranties["monitor"])
    record["mouse"].append(warranties["mouse"])
    record["keyboard"].append(warranties["keyboard"])
    record["speakers"].append(warranties["speakers"])
    record["webcam"].append(warranties["webcam"])

    try:
        record["pcdt-id"] = primary_key
        record["date"]    = datetime.now().strftime("%d-%m-%Y")
        
        mycoll.insert_one(record)
        generate_report(primary_key+".pdf", record)

        # receiver_email = mydb["users"].find_one()
        # send_email([], primary_key+".pdf")
        
        base64_pdf = base64.b64encode(open(f"{primary_key}.pdf","rb").read())
        
        return jsonify({
            "filename" : f"{primary_key}.pdf", 
            "data" : base64_pdf.decode("utf-8") 
        })

    except Exception as e:
        # print("Error occured !")
        # print(traceback.format_exc())
        # print(e)
        status_code = Response(status=400)
        return status_code

@app.route('/modify_data', methods=["POST","GET"])
@login_required
def modify_data():
    record = request.json

    result = {}

    for key in record.keys():
        if isinstance(record[key], list) and not record[key][1].strip():
            result[key] = "Empty"
        elif isinstance(record[key], str) and not record[key].strip():
            result[key] = "Empty"

    if bool(result):
        result["msg"] = "Fill the Red Highlighted Fields!"
        return jsonify(result), 400

    #================================================================== 
    #  Regex Pay Roll Check
    #================================================================== 
    payroll = re.compile("^PR\d{5}")
    
    record["custodian-payroll"] = record["custodian-payroll"].upper()

    if not bool(payroll.match(record["custodian-payroll"])):
        result["custodian-payroll"] = "Empty"
        result["msg"] = "Pay Roll Number is Not in Correct Format!"
        return jsonify(result), 400
    #==================================================================

    #================================================================== 
    #  Regex PO Number Check
    #================================================================== 
    ponumber = re.compile("^\d{14}|\d{4}E\d{9}")

    record["coins-po-number"] = record["coins-po-number"].upper()
    record["gem-po-number"] = record["gem-po-number"].upper()
    
    if not bool(ponumber.match(record["coins-po-number"])):
        result["coins-po-number"] = "Empty"
        result["msg"] = "Coins PO Number is Not in Correct Format!"
        return jsonify(result), 400
    #==================================================================

    warranties = list(mydb["warranty"].find({},{"_id":0,"part":1, "period":1}))    
    warranties = dict(
        zip( [doc["part"] for doc in warranties] ,
        [doc["period"] for doc in warranties])
    )

    try:        

        result = mycoll.find_one_and_update({"_id":record["_id"]},{
            "$set" : {
                    "_id"               :   record["_id"] ,
                    "custodian-payroll" :   record["custodian-payroll"] ,
                    "custodian-email"   :   record["custodian-email"] ,
                    "custodian-name"    :   record["custodian-name"] ,
                    "asset-id"          :   record["asset-id"] ,
                    "custodian-mobile"  :   record["custodian-mobile"] ,
                    "coins-po-number"   :   record["coins-po-number"] ,
                    "gem-po-number"     :   record["gem-po-number"] ,
                    "cpu"               :   [ record["cpu"][0],         record["cpu"][1]            ,warranties["cpu"]] ,
                    "motherboard"       :   [ record["motherboard"][0], record["motherboard"][1]    ,warranties["motherboard"]] ,
                    "ram"               :   [ record["ram"][0],         record["ram"][1]            ,warranties["ram"]] ,
                    "hdd"               :   [ record["hdd"][0],         record["hdd"][1]            ,warranties["hdd"]] ,
                    "ssd"               :   [ record["ssd"][0],         record["ssd"][1]            ,warranties["ssd"]] ,
                    "smps"              :   [ record["smps"][0],        record["smps"][1]           ,warranties["smps"]] ,
                    "cabinet"           :   [ record["cabinet"][0],     record["cabinet"][1]        ,warranties["cabinet"]] ,
                    "monitor"           :   [ record["monitor"][0],     record["monitor"][1]        ,warranties["monitor"]] ,
                    "mouse"             :   [ record["mouse"][0],       record["mouse"][1]          ,warranties["mouse"]] ,
                    "keyboard"          :   [ record["keyboard"][0],    record["keyboard"][1]       ,warranties["keyboard"]] ,
                    "speakers"          :   [ record["speakers"][0],    record["speakers"][1]       ,warranties["speakers"]] ,
                    "webcam"            :   [ record["webcam"][0],      record["webcam"][1]         ,warranties["webcam"]] ,
                    "deo"               :   record["deo"] 
                }
        }, new=True)

        if result:
            if os.path.exists(f"{record['_id']}.pdf"):
                os.remove(f"{record['_id']}.pdf")

            generate_report(f"{record['_id']}.pdf", result)
            msg = f"PCDT-ID {record['_id']}<br>Record Updated!"
            return jsonify({
                "msg":msg,
                "type":"msg"
                })
        else:
            string = f"PCDT-ID {record['_id']}<br>Record Not Found!"
            return jsonify({"msg" : string}) , 400
            
    except Exception as e:
        print("Error occured !")
        print(traceback.format_exc())
        print(e)
        return jsonify({"msg" : "Server Error!"}) , 400


@app.route('/download_report', methods=["POST"])
@login_required
def download_report():
    filename = request.json["filename"]

    if not os.path.exists(f"{filename}.pdf"):
        data = mycoll.find_one({"_id":filename})
        generate_report(f"{filename}.pdf", data)

    base64_pdf = base64.b64encode(open(f"{filename}.pdf","rb").read())

    return jsonify({
                "type"     : "file",
                "filename" : f"{filename}.pdf", 
                "data" : base64_pdf.decode("utf-8") 
            })


@app.route('/email_report', methods=["POST"])
@login_required
def email_report():
    filename = request.json["filename"]
    to = request.json["to"]
    send_email([to],f"{filename}.pdf",sender=current_user.username)

    return jsonify({
                "type"     : "email",
                "msg"      : "Email Sent!"
            })

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=443,
        # debug=True,
        ssl_context=('cert.pem', 'key.pem')
    ) 