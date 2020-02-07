from django.shortcuts import render
from django.http import HttpResponse
import pyqrcode
from globalapp import models
import os

def home(request):
    return render(request,'mainpage.html',{"name":"Pavan"})

def teacher(request):
    return render(request,'home.html')

def generateqr(request):

    imagename = "myqr.png"
    courseno = request.POST['courseno']
    day = request.POST['day']
    month = request.POST['month']
    year = request.POST['Year']
    
    date = "D" + day + "M" + month + "Y" + year

    s = courseno+" "+date
    
    url = pyqrcode.create(s)  
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR,'static')
    IMG_ROOT = os.path.join(MEDIA_ROOT,imagename)
    loc = str(IMG_ROOT)

    url.png(loc, scale = 8)


        
    studentsno = models.NS101.objects.all()
    count = 0
    for p in studentsno:
        count += getattr(p,date)

    return render(request,"qrdisplaypage.html",{"imagename":"myqr.png","s":s,"count":count})

