import os
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from PIL import Image

def load_encodings():
    known_face_encodings = []
    known_face_names = []
    image_directory = os.path.join("Face", "Images")

    if not os.path.exists(image_directory):
        print(f"Directory not found: {image_directory}")
        return known_face_encodings, known_face_names

    print(f"Directory found: {image_directory}")

    for name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, name)
        print(f"Processing image: {image_path}")

        try:
            # Convert image to RGB format using PIL
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    rgb_img = img.convert("RGB")
                    rgb_img.save(image_path)
                print(f"{name}: converted to RGB format")

            # Load the image with face_recognition
            image = face_recognition.load_image_file(image_path)

            # Ensure image is in RGB format
            if image.ndim != 3 or image.shape[2] != 3:
                print(f"Skipping unsupported image format: {name}")
                continue

            try:
                encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(encoding)
                known_face_names.append(os.path.splitext(name)[0])
            except IndexError:
                print(f"No face found in image: {name}")

        except Exception as e:
            print(f"Error processing {name}: {e}")

    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_encodings()

video_capture = cv2.VideoCapture(0)

def mark_attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

while True:
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            mark_attendance(name)

        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
