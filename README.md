# Problem Definition:
Make a web application to detect faces from Web Camera.
## Task Description:
* Use OpenCV for face detection
* Create a web server that call the open cv application and show the video stream on the browser
* Crop the detected face and save it in a folder
* Create a database that will save the address of the image and time stamp.

## Technology:
* Python
* OpenCV
* Flask/Quart/FastAPI
* MongoDB/SQL

## Usage

This webapp launches theserver webcam and broadcasts it to the client. It detects the first frame that contains an image and store it under public/faceimages with an uniquely generated file name. The unique name is stored into MongoDB along side with timestamp.

1. Install the packages in [requirements](requirements.txt)
2. Create a MongoDB database named 'facedetection' with a collection 'faces'
3. Run the server with: flask run
4. Visit localhost:5000
