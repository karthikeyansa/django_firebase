from django.shortcuts import render,redirect
import pyrebase
from django.contrib import auth as Auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
config ={
    'apiKey': "AIzaSyAOJGjT-1Umc7i6SuGBVomJU-nWfUYhGs4",
    'authDomain': "django-c9216.firebaseapp.com",
    'databaseURL': "https://django-c9216.firebaseio.com",
    'projectId': "django-c9216",
    'storageBucket': "django-c9216.appspot.com",
    'messagingSenderId': "424754483306",
    'appId': "1:424754483306:web:b14e7a7a39d7ce849f3a13",
    'measurementId': "G-0D508PHZW3"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
database = firebase.database()

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.sign_in_with_email_and_password(email, password)
        if user:
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            return redirect(welcome,email = email)
    return render(request,'mysite/signin.html')

def newuser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            newuser = auth.create_user_with_email_and_password(email,password)
            if newuser:
                uid = newuser['localId']
                data = {'name':name,'status':'1'}
                database.child("users").child(uid).child("details").set(data)
                messages.add_message(request,messages.SUCCESS,'Profile created successfully.')
                return render(request,'mysite/signin.html')
        except:
            messages.add_message(request, messages.WARNING, 'wrong credentials.')
            return render(request,'mysite/signup.html')
    return render(request,'mysite/signup.html')

def welcome(request,email):
        return render(request,'mysite/welcome.html',{'email':email})
def logout(request):
    del request.session['uid']
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully.')
    return redirect(signin)

@csrf_exempt
def post_report(request):
    try:
        request.session['uid']
        if request.method == 'POST':
            title,progress = request.POST.get('title'),request.POST.get('progress')
            idtoken = request.session['uid']
            user = auth.get_account_info(idtoken)
            email,user = user['users'][0]['email'],user['users'][0]['localId']
            timestamp = str(datetime.timestamp(datetime.now()))[:10]
            data = {
                'title':title,'progress':progress
            }
            database.child("users").child(user).child("reports").child(str(timestamp)).set(data)
            return redirect(welcome,email = email)
    except:
        messages.add_message(request, messages.SUCCESS, 'Invalid credentials Login again.')
        return redirect(signin)
def check_report(request):
    idtoken = request.session['uid']
    user = auth.get_account_info(idtoken)
    email, user = user['users'][0]['email'], user['users'][0]['localId']
    data = sorted(list(database.child("users").child(user).child("reports").shallow().get().val()),reverse=True)
    tasks = []
    for i in data:
        task = database.child("users").child(user).child("reports").child(i).get().val()
        tasks.append(task)
    print(tasks)
    return render(request,'mysite/welcome.html',{'email':email,'tasks':tasks})
