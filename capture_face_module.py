import cv2
import os
import numpy as np


def capture_face(prototxt_path="./deploy.prototxt", model_path="./res10_300x300_ssd_iter_140000_fp16.caffemodel"):
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    face_roi = None  # Placeholder for the detected face
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        net.setInput(blob)
        detections = net.forward()

        detected_face = False

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.99:  # Confidence threshold
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x, y, x1, y1) = box.astype("int")

                face_roi = frame[y:y1, x:x1]
                face_roi_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                face_roi_resized = cv2.resize(face_roi_gray, (100, 100))  # Resize to (100, 100)

                detected_face = True
                break

        cv2.imshow('Video', frame)

        if detected_face or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    if detected_face:
        return face_roi_resized  # Return gray-scaled and resized face as numpy array
    else:
        return None
    
def capture_multiple_faces(prototxt_path="./deploy.prototxt", model_path="./res10_300x300_ssd_iter_140000_fp16.caffemodel"):
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    captured_faces = []  # List to hold captured face images

    counter = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.98:  # Adjusted confidence threshold to 98%
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x, y, x1, y1) = box.astype("int")
                cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

                face_roi = frame[y:y1, x:x1]
                face_roi_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
                face_roi_resized = cv2.resize(face_roi_gray, (100, 100))  # Resize to (100, 100)
                captured_faces.append(face_roi_resized)  # Append numpy array to list
                counter += 1
                if counter >= 100:
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return captured_faces  # Return list of captured faces

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return captured_faces  # Return list of captured faces, even if <100 faces captured
