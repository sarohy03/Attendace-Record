import os
import json
import csv
import base64
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import face_recognition

# Load encodings and names when the module is imported
with open('D:/4th semseter/lay/project_ai/attendence_system/LMS/face_encodings.json', 'r') as f:
    data = json.load(f)
known_face_encodings = [np.array(encoding) for encoding in data['encodings']]
known_faces_names = data['names']

def home(request):
    return render(request, 'index.html')

def courses(request):
    return render(request, 'courses.html')

def news(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'aboutUs.html') 

def NoFace(request):
    return render(request, 'NoFace.html') 

@csrf_exempt
def attendence(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        course = request.POST.get('course')

        # Decode the base64 image data
        image_data = image_data.split(',')[1]
        image = Image.open(BytesIO(base64.b64decode(image_data)))

        # Convert image to array
        unknown_image = np.array(image)

        # Get face encodings from the uploaded image
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        if not unknown_encoding:
            return render(request, 'NoFace.html')

        unknown_encoding = unknown_encoding[0]

        # Compare the unknown image with known faces
        matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
        name = "Unknown"
        if any(matches):
            name = known_faces_names[matches.index(True)]

        # Get the current date for the CSV filename
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")

        # Open a CSV file to write attendance
        file_path = f'data/{current_date}-{course}.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_exists = os.path.isfile(file_path)
        marked_names = []

        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                marked_names = [row[0] for row in reader]
        except FileNotFoundError:
            pass

        with open(file_path, 'a+', newline='') as f:
            lnwriter = csv.writer(f)
            if not file_exists:
                lnwriter.writerow(['Name', 'Time', 'Course'])
            if name not in marked_names:
                lnwriter.writerow([name, current_time, course])

        return render(request, 'index.html')

    elif request.method == 'GET':
        return render(request, 'attendence.html')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def display_csv_files(request):
    # Directory containing the CSV files
    data_dir = os.path.join(settings.BASE_DIR, 'data')

    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

    # Prepare the data to be passed to the template
    csv_data = {}
    for csv_file in csv_files:
        file_path = os.path.join(data_dir, csv_file)
        df = pd.read_csv(file_path)
        csv_data[csv_file] = df.to_html(index=False, escape=False)

    # Render the template with the csv_data
    return render(request, 'display_csv_files.html', {'csv_data': csv_data})

# def attendence(request):
#     if request.method == 'POST':
#         image_data = request.POST.get('image_data')
        
#         if not image_data:
#             return JsonResponse({'status': 'error', 'message': 'No image data provided'})

#         # Decode the base64 image data
#         image_data = image_data.split(',')[1]
#         image = Image.open(BytesIO(base64.b64decode(image_data)))

#         # Convert image to array
#         unknown_image = np.array(image)

#         # Get face encodings from the uploaded image
#         unknown_encoding = face_recognition.face_encodings(unknown_image)

#         if not unknown_encoding:
#             return JsonResponse({'status': 'error', 'message': 'No face found in the image'})

#         unknown_encoding = unknown_encoding[0]

#         # Compare the unknown image with known faces
#         matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
#         name = "Unknown"
#         if any(matches):
#             name = known_faces_names[matches.index(True)]

#         # Get the current date for the CSV filename
#         now = datetime.now()
#         current_date = now.strftime("%Y-%m-%d")
#         current_time = now.strftime("%H:%M:%S")

#         # Open a CSV file to write attendance
#         file_path = f'data/{current_date}.csv'
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         file_exists = os.path.isfile(file_path)
#         marked_names = []

#         try:
#             with open(file_path, 'r') as f:
#                 reader = csv.reader(f)
#                 marked_names = [row[0] for row in reader]
#         except FileNotFoundError:
#             pass

#         with open(file_path, 'a+', newline='') as f:
#             lnwriter = csv.writer(f)
#             if not file_exists:
#                 lnwriter.writerow(['Name', 'Time'])
#             if name not in marked_names:
#                 lnwriter.writerow([name, current_time])

#         return render(request, 'index.html')

#     elif request.method == 'GET':
#         return render(request, 'attendence.html')
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})