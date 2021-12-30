from typing import Collection
from flask import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_mongoengine import MongoEngine
from flask_qrcode import QRcode
import pymongo
import os
from form import LoginForm
from werkzeug.urls import url_parse
import re
from datetime import datetime

from colorama import init, Fore, Back, Style
init()

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
    print(os.path.join(app.root_path, 'static/img'))
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
        
        user = User.objects(username=form.username.data,password=form.password.data).first()

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
        mousekey_list    = sorted(list(mydb['mousekey'].distinct("brand")))

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
                            mousekey_list = mousekey_list
                            )

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_data', methods=["POST"])
def add_data():
    record = request.json
    print(record)

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
    
    record["custodian"] = record["custodian"].upper()

    if not bool(payroll.match(record["custodian"])):
        result["custodian"] = "Empty"
        result["msg"] = "Pay Roll Number is Not in Correct Format!"
        return jsonify(result), 400
    #==================================================================

    #================================================================== 
    #  Regex PO Number Check
    #================================================================== 
    ponumber = re.compile("^PRAA\d{14}|PRAA\d{4}E\d{9}")

    record["po-number"] = record["po-number"].upper()
    
    if not bool(ponumber.match(record["po-number"])):
        result["po-number"] = "Empty"
        result["msg"] = "PO Number is Not in Correct Format!"
        return jsonify(result), 400
    #==================================================================

    primary_key = datetime.now().strftime("%Y%m%d%f")
    record["_id"] = primary_key

    try:
        mycoll.insert_one(record)
        # status_code = Response(status=201)
        return render_template("qrcode.html", primary_key=primary_key)

    except Exception as e:
        # print("Error occured !")
        # print(e)
        status_code = Response(status=400)
        return status_code

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=443,
        # debug=True,
        ssl_context=('cert.pem', 'key.pem')
    ) 