#import redis
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_kvsession import KVSessionExtension
#from simplekv.memory.redisstore import RedisStore
from simplekv.fs import FilesystemStore
import logging

#store = RedisStore(redis.StrictRedis())
store = FilesystemStore('./datastore')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'df61f5fe12eb40792e85b284ead07d51'
bcrypt = Bcrypt(app)

#KVSessionExtension(store, app)
# KVSessionExtension(store, app)

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s:\t%(message)s')

from app.flask_web import routes_webgui
from app.flask_web import routes_api
