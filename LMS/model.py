import face_recognition
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

def process_images_from_folder(folder_path):
    all_encodings = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            print(f"Processing image: {file_name}")
            image = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            all_encodings[file_name] = face_encodings
            display_image_with_boxes(file_path, face_locations)
    return all_encodings



folder_path = r'D:\4th semseter\lay\project_ai\attendence_system\LMS\known_face'
encodings = process_images_from_folder(folder_path)

for file_name, encoding_list in encodings.items():
    print(f"Encodings for {file_name}:")
    for i, encoding in enumerate(encoding_list):
        print(f"  Face {i + 1}: {encoding}")
    print()

import json
with open('encodings.json', 'w') as f:
    json.dump({k: [e.tolist() for e in v] for k, v in encodings.items()}, f)
