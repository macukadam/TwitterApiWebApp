from django.shortcuts import render
from .models import Disaster_Type, User_Location, Location
from django.http import Http404, HttpResponse, JsonResponse
from django.core.validators import validate_email
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import tweets
from django.db.models import Func, F
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def index(request):
    return render(request, 'TweetUtils/index.html')

def sendmail(request):
    email = EmailMessage('title', 'body', to=['twasterapp@gmail.com'])
    email.send()

@login_required
def detail(request):
    try :
        usrlocations = User_Location.objects.filter(User = request.user)
        loc_ids = []
        for loc in usrlocations:
            loc_ids.append(loc.Location_id)
        locs = Location.objects.filter(id__in = loc_ids)
    except User_Location.DoesNotExist:
         raise Http404("User does not exists")
    return render(request, 'TweetUtils/detail.html',{'locations':locs})

@login_required
def deletecity(request):
    if request.method == 'POST':
        city_id = request.POST.get('city_id')
        deletedcity = User_Location.objects.filter(User = request.user, Location_id = city_id).delete()
        
    return JsonResponse({"inlist":False,"locid":city_id })

@login_required
def addlocation(request):
    try :
        usrlocations = User_Location.objects.filter(User = request.user)
    except User_Location.DoesNotExist:
         raise Http404("User does not exists")
    if request.method == 'POST':
        title = request.POST.getlist('locations[title][]')
        long = request.POST.getlist('locations[long][]')
        lat = request.POST.getlist('locations[lat][]')
        location = Location.objects.annotate(abs_diff=Func((F('Latitude') - lat[0])**2 + (F('Longitude') - long[0])**2, function='ABS')).order_by('abs_diff').first()
        if len(usrlocations) > 30:
            return JsonResponse({"inlist":True, "message":"Adding more than 30 locations to your list is not allowed"})
        for loc in usrlocations:
            if loc.Location_id==location.id:
                return JsonResponse({"inlist":True, "message":"{0} is allready in your list".format(location.City)})
        
        locationinfo = {
        'id': location.id,
        'city': location.City,
        'country': location.Country,
        }

        User_Location.objects.create(User= request.user,Location = location)
    return JsonResponse({"inlist":False, "message":"{0} is successfully added to your list".format(location.City),"loc":locationinfo })

def create_user(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        checks = True
        
        try:
            validate_email(email)
        except forms.ValidationError:
            jresponse = JsonResponse({"redirect":False, "error_message":"Email is not valid"})
            checks = False
        if len(name) < 4:
            jresponse = JsonResponse({"redirect":False, "error_message":"User name must be longer than 4 characters"})
            checks = False
        if len(password) < 7:
            jresponse = JsonResponse({"redirect":False, "error_message":"Password must be at least 7 characters long"})
            checks = False
        if not any(char.isdigit() for char in password):
            jresponse = JsonResponse({"redirect":False, "error_message":"Password must contain at least 1 digit"})
            checks = False
        if not any(char.isalpha() for char in password):
            jresponse = JsonResponse({"redirect":False, "error_message":"Password must contain at least 1 letter"})
            checks = False

        if not get_or_none(User,username = name) is None:
            # at least one object satisfying query exists
            jresponse =  JsonResponse({"redirect":False, "error_message":"The user name has taken"})
            checks = False
        elif not get_or_none(User,email = email) is None:
            # no object satisfying query exists
            jresponse = JsonResponse({"redirect":False, "error_message":"E-mail is already in use"})
            checks = False
        else:
            
            if checks == True:
                User.objects.create_user(
                username = name,
                email = email,
                password = password
                )
                jresponse = JsonResponse({"redirect":True,"redirect_url":"/TweetUtils"})
        return jresponse

def user_login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"redirect":True,"redirect_url":"/TweetUtils"})
        else:
            return JsonResponse({"redirect":False, "error_message":"Wrong credentials"})
        
def user_logout(request):
    logout(request)
    return JsonResponse({"redirect":True,"redirect_url":"/TweetUtils"})