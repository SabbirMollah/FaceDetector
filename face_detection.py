import cv2

class FaceDetector:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('static/classifiers/haarcascade_frontalface_default.xml')

    def hasFace(self, img):

        # This classifier can detect faces only from Grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        img_cropped = img

        faceFound = True if len(faces) else False
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            img_cropped = img[y:y+h, x:x+h]
        # Display the output
        # cv2.imshow('img', img)
        
        return (faceFound, img, img_cropped)


if __name__ == "__main__":

    img = cv2.imread("cat.jpg")
    faceDetected = FaceDetector().hasFace(img)

    if faceDetected:
        print("Face found")
    else:
        print("Face Not found")