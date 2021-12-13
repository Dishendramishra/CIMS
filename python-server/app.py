from typing import Collection
from flask import *
from flask_mongoengine import MongoEngine
import pymongo
import os
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from pymongo import response

DOMAIN = "localhost"
DATABASE = "prlcts"
COLLECTION = "inventory"
# MONGOUSER   = os.environ["MONGOUSER"]
# MONGOPASSWD = os.environ["MONGOPASSWD"]

app = Flask(__name__, template_folder='templates')

# ==================================================================
#                           MongoDB Setup
# ==================================================================
app.config['MONGODB_SETTINGS'] = {
    'db'  : DATABASE,
    'host': 'localhost', #os.environ["MONGOIP"],
    'port': 27017,
}
app.secret_key = "nothing"

# db = MongoEngine()
# db.init_app(app)

# class User(UserMixin,db.Document):
#     meta = {"collection":"keys"}
#     key = db.StringField()

myclient = pymongo.MongoClient(
    "mongodb://{}:27017/".format(DOMAIN), 
    # username = MONGOUSER,
    # password = MONGOPASSWD
    )

mydb = myclient[DATABASE]
mycoll = mydb[COLLECTION]
# ==================================================================

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
    # app.run(debug=True)
    app.run(
        host="0.0.0.0",
        port=443,
        debug=True,
        ssl_context=('cert.pem', 'key.pem')
    ) 