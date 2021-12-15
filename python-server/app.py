from typing import Collection
from flask import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_mongoengine import MongoEngine
import pymongo
import os
from form import LoginForm
from werkzeug.urls import url_parse
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
    return render_template("form.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_data', methods=["POST"])
def add_data():
    record = request.json
    print(record)    
    try:
        mycoll.insert_one(record)
        status_code = Response(status=201)
        return status_code

    except Exception as e:
        # print("Error occured !")
        # print(e)
        status_code = Response(status=400)
        return status_code

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=443,
        ssl_context=('cert.pem', 'key.pem')
    ) 