from flask import Flask, render_template, Response, flash, url_for, request, redirect, send_file
import cv2
from face_detection import FaceDetector
import os
from flask_pymongo import PyMongo
from pymongo import MongoClient

from datetime import datetime
import secrets

UPLOAD_FOLDER = './public/faceimages/'

app = Flask(__name__)

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["facedetection"]
face_collection = mydb["faces"]

secret = secrets.token_urlsafe(32)
app.secret_key = secret

camera = cv2.VideoCapture(0)


# Initialized here to avoid reloading the classifier every thread
faceDetector = FaceDetector()

def save_face_to_database(img):
    try:
        face = {"timestamp": str(datetime.now())}
        
        x = face_collection.insert_one(face)
        cv2.imwrite(UPLOAD_FOLDER+ str(x.inserted_id) + ".jpg", img)
        
    except Exception as ex:
        print(ex)
    
    print("Image saved to database")

def gen_frames():  
    face_saved_to_database = False

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            face_found, img, img_cropped = faceDetector.hasFace(frame)


            if face_found and not face_saved_to_database:
                save_face_to_database(img_cropped)
                face_saved_to_database = True
            
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face/<id>')
def send_face_image(id):
    return send_file(UPLOAD_FOLDER + id +".jpg")

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5000)