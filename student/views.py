from PIL import Image
from pyzbar.pyzbar import decode
import sqlite3
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from globalapp import models
from django.db import connection
import os
from django.urls import path, include
import face_recognition
import cv2 
from globalapp.models import Profile


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return render(request,"upload.html",{"username":username})
    
    else:
        return render(request,"register.html")


def upload(request):
    
    if request.method == "POST":
        
        username = request.POST['username']
        uuser = User.objects.get(username = username)
        profile = Profile.objects.get(user = uuser)
        profile.head_shot = request.FILES['pic']
        profile.save()

        return render(request,"mainpage.html")

    else:
        return redirect("login")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MEDIA_ROOT =os.path.join(BASE_DIR,'media\profile_images')
            IMG_ROOT =os.path.join(MEDIA_ROOT,username)
            loc=(str(IMG_ROOT)+".jpg")


            if facedect(loc):
                return render(request,"qrscan.html",{"username":username,"password":password})

            else:
                    messages.info(request,'Face not matched')
                    return redirect("login")
        else:
            messages.info(request,'Invalid credentials')
            return redirect("login")

    else:
        return render(request,"login.html")


def qrscan(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        imagename = "myqr.png"
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR,'static')
        IMG_ROOT = os.path.join(MEDIA_ROOT,imagename)
        loc = str(IMG_ROOT)
        
        d = decode(Image.open(loc))

        a = d[0][0].decode("utf-8") 
        CSVfilename = a[0:5]
        date = a[6:]

        toedit = models.NS101.objects.get(roll = username)
        setattr(toedit,date,1)
        toedit.save()



        return render(request,"afterscan.html",{"username":username,"coursecode":CSVfilename ,"date" :date})



def facedect(loc):
        cam = cv2.VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:    
                # frame captured without any errors
                cv2.namedWindow("cam-test")
                cv2.imshow("cam-test",img)
                #cv2.waitKey(0)
                cv2.destroyWindow("cam-test")
                cv2.imwrite("filename.jpg",img)

                
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)

                print(check)

                if check[0]:
                        return True

                else :
                        return False    
























