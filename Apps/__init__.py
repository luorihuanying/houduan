# This Python file uses the following encoding: utf-8
import os
from PIL import Image
from threading import Lock
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from Apps import settings
from Apps.apis import api_init
from Apps.ext import ext_init
from Apps.settings import envs, Config
from flask_cors import CORS
from config import DB_URI
from sqlalchemy import create_engine
eng = create_engine(DB_URI)
from Apps.ext import db

app = Flask(__name__)

CORS(app)
# app.config.from_object(envs.get(env))
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = False

api_init(app)
ext_init(app)

async_mode = None
socketio = SocketIO(app,async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    temp = []
    while True:
        socketio.sleep(5)
        with eng.connect() as con:
            res = con.execute("select*from historydatas order by createTime desc limit 1")
            for row in res:
                if row:
                    temp.append(row)
                    if len(temp) == 1:
                        socketio.emit("server_response", {"id": str(row[0]),"createTime":str(row[4]),"data":str(row[5])},namespace='/socketio')

                    else:
                        if str(temp[0]) != str(temp[1]):
                            socketio.emit("server_response", {"id": str(temp[1][0]),"createTime":str(temp[1][4]),"data":str(temp[1][5])},namespace='/socketio')
                            del temp[0]
                        else:
                            del temp[0]
                            # socketio.emit("server_response",
                            #               {"id": '0', "createTime": str(datetime.now()), "data": '0'},
                            #               namespace='/socketio')
                else:
                    pass

@socketio.on('connect', namespace='/socketio')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@app.errorhandler(404)
def catchInnerError(error):

    return error

@app.route('/')
def index():
    return render_template('index.html',async_mode=socketio.async_mode)

@app.route('/showTifImage')
def showTifImage():
    imgPath = os.getcwd()+r'\Apps\static\tifToPng'
    dir = os.listdir(imgPath)
    #每行显示图片数
    hang = 8
    H = len(dir)+1
    L = len(dir)
    # width = 400
    # height = 400
    return render_template('test.html',dir = dir,hang = hang,H = H,L=L)

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)
