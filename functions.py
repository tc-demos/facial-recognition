import cv2

def detectFacesStill():
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

    image = cv2.imread('./people.jpg')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.namedWindow("AAAAA")

    cv2.imshow("AAAAA", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detectFacesVideo():
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./cascades/haarcascade_eye.xml')

    cv2.namedWindow("Video")

    camera = cv2.VideoCapture(0)

    while cv2.waitKey(1) == -1:
        success, frame = camera.read()

        if success:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(120,120))

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,  y+h),   (255,0,0),2)

                roi_gray = gray[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.03,5,minSize = (40,40))

                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(frame, (x+ex,y+ey),   (x+ex+ew,  y+ey+eh), (0,255,0), 2)

            cv2.imshow("Video", frame)
    cv2.destroyAllWindows()


def generateData():
    import os

    MAX_FRAMES = 200

    initials = input("Enter your initials (e.g. JC): ")
    output_folder = f"./data/{initials}"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')

    camera = cv2.VideoCapture(0)

    count = 0

    while cv2.waitKey(1) == -1 and count < MAX_FRAMES:
        success, frame = camera.read()

        if success:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(120,120))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                face_image = cv2.resize(gray[y:y+h, x:x+w], (200,200))
                face_filename = f"{output_folder}/{count}.pgm"
                cv2.imwrite(face_filename, face_image)
                count += 1

            cv2.imshow('Capturing faces...', frame)

    cv2.destroyAllWindows()