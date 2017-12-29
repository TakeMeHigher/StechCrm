from django.shortcuts import render,HttpResponse,redirect
from app01 import models
# Create your views here.

def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        print(name,pwd)
        user=models.UserInfo.objects.filter(username=name,password=pwd).first()
        stu=models.Student.objects.filter(username=name,password=pwd).first()

        if user:
            request.session['user']={'name':name,'id':user.id}
            return HttpResponse('ok')
        elif stu:
            print(123)
            request.session['stu'] = {'name': name, 'id': stu.id}
            return redirect('/stark/app01/studyrecord/?student=%s'%stu.id)
        else:
            return render(request,'login.html',{"msg":'用户名或密码不正确'})


