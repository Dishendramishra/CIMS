from typing import Collection
from flask import *
from flask_mongoengine import MongoEngine
import pymongo
import os
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from pymongo import response

CIMS_DOMAIN      = os.environ["CIMS_DOMAIN"]
CIMS_DATABASE    = os.environ["CIMS_DATABASE"]
CIMS_COLLECTION  = os.environ["CIMS_COLLECTION"]
CIMS_MONGOUSER   = os.environ["CIMS_MONGOUSER"]
CIMS_MONGOPASSWD = os.environ["CIMS_MONGOPASSWD"]
FLASK_SEC_KEY    = os.environ["FLASK_SEC_KEY"]

app = Flask(__name__, template_folder='templates')

# ==================================================================
#                           MongoDB Setup
# ==================================================================
app.config['MONGODB_SETTINGS'] = {
    'db'  : CIMS_DATABASE,
    'host': FLASK_SEC_KEY,
    'port': 27017,
}
app.secret_key = FLASK_SEC_KEY

# db = MongoEngine()
# db.init_app(app)

# class User(UserMixin,db.Document):
#     meta = {"collection":"keys"}
#     key = db.StringField()

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
def home():
    return render_template("view.html")

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