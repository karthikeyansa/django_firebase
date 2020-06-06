from django.shortcuts import render,redirect
from firebase import firebase

firebase = firebase.FirebaseApplication("https://testing-9807a.firebaseio.com/",None)

def post(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        data = {
            'name':name,
            'age':age
        }
        result = firebase.post('/testing-9807a/User', data)
        print(result)
        return redirect(post)
    result = firebase.get('/testing-9807a/User', '')
    print(result)
    return render(request, 'mysite/index.html', {'datas': result})
