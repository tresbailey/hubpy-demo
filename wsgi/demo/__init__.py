__author__ = 'tresback'

import json
import redis
import uuid
from flaskext.mongoalchemy import MongoAlchemy
from flask import Flask, request, url_for, session, flash,\
    render_template
import os


app = Flask(__name__)
app.debug = True

@app.before_request
def convert_json():
    if request.data and request.data is not None:
        request.data = json.loads(request.data)


@app.after_request
def add_headers(response):
    if isinstance(response.data, dict) or isinstance(response.data, list):
        response.headers['Content-Type'] = 'application/json'
    response.headers.add_header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers.add_header('Access-Control-Allow-Origin', '*')
    response.headers.add_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    print 'response headers are %s' % response.headers
    return response

# Initialize the MongoDB connection info and set it onto the app for flask-mongoalchemy
app.config['MONGOALCHEMY_SERVER'] = os.environ.get('OPENSHIFT_MONGODB_DB_HOST', 'localhost')
# Notice how we read the env variables setup by the MongoDB cartridge
app.config['MONGOALCHEMY_PORT'] = int(os.environ.get('OPENSHIFT_MONGODB_DB_PORT', 27017))
app.config['MONGOALCHEMY_DATABASE'] = os.environ.get('MONGO_DB', 'demodb')
app.config['MONGOALCHEMY_USER'] = os.environ.get('OPENSHIFT_MONGODB_DB_USERNAME')
app.config['MONGOALCHEMY_PASSWORD'] = os.environ.get('OPENSHIFT_MONGODB_DB_PASSWORD')
app.config['MONGOALCHEMY_SERVER_AUTH'] = True

db = MongoAlchemy(app)

# A secret key should be setup for OpenShift
app.secret_key = str(uuid.uuid4())
DEBUG = True

# Again, the redis cartridge requires these environment variables
redis_cli = redis.Redis(host=os.environ.get('OPENSHIFT_REDIS_DB_HOST', 'localhost'), 
        port=int(os.environ.get('OPENSHIFT_REDIS_DB_PORT', '6379')),
        password=os.environ.get('REDIS_PASSWORD', None))

# The openshift DNS name is also in a variable.  Use it if we're there
HOME_URL = os.getenv('OPENSHIFT_GEAR_DNS', 'http://localhost')
if 'http' not in HOME_URL:
    # OpenShift will always deploy as SSL by default, so let's make use
    HOME_URL = "https://%s" % HOME_URL

from demo.views.api import api
app.register_blueprint(api)

if __name__ == '__main__':
    app.run('127.0.0.1')
