from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from .models import *

# Create your views here.

def entry(request):
    if request.user.is_authenticated:
        return render(request,'./note_system/index.html')
    return render(request, './note_system/login_page.html')

def register(request):

    if request.method == 'POST':
        if createUser(request,request.POST['email'], password = request.POST['password']):
                context = {'username':request.POST['email']}
                return render(request,'./note_system/index.html',context)
        return HttpResponse("Địa chỉ email của bạn đã được đăng ký từ trước. Xin bạn vui lòng chọn địa chỉ email khác !")
            
def login_process(request):
    if request.method == 'POST':
        tmp_user = authenticate(username = request.POST['email'], password = request.POST['password'])
        if tmp_user is None:
            return HttpResponse("Tài khoản hoặc mật khẩu không chính xác !")

        login(request, tmp_user)
        # get note items belong to user and pass it into index file
        noteitems = []
        for item in NoteItem.objects.all():
            if item.owner.email == request.POST['email']:
                noteitems.append(item)
                
        context = {'username':request.POST['email'], 'noteitems':noteitems, 'total_notes':len(noteitems)}
        return render(request, './note_system/index.html', context)
    elif request.user.is_authenticated:
        noteitems = []
        for item in NoteItem.objects.all():
            if item.owner.username == request.user.username:
                noteitems.append(item)
                
        context = {'username':request.user.username, 'noteitems':noteitems, 'total_notes':len(noteitems)}
        return render(request, './note_system/index.html', context)


def logout_process(request):
    if request.method == 'GET':
        logout(request)
        return render(request, './note_system/login_page.html')

def createUser(request, email, password):
    userName = email
    userMail = email
    userPass = password

    try:
        tmp_user = User.objects.get(username = email)
        return False
    except:
        
        user = User.objects.create_user(userName, userMail ,userPass)
        user.save()
        login(request, user)
        customuser = Customer(user = user, email = email)
        customuser.save()
        return True

def go_to_new_note_page(request):
    context = {'username':request.user.username}
    return render(request, './note_system/new_note.html',context)

def add_new_note(request):
    if request.method == 'GET':
        print(request.user)
        note_subject = request.GET['note_subject']
        note_content = request.GET['note_content']
        note_item = NoteItem(owner = request.user, subject = note_subject, content = note_content)
        note_item.save()
        return redirect('/login/')

def delete_note(request, note_id):
    item = NoteItem.objects.get(id = note_id)
    item.delete()
    return redirect('/login/')

def edit_note(request, note_id, type):
    if type == 1:
        context = {'username':request.user.username, 'item':NoteItem.objects.get(id = note_id)}
        return render(request, './note_system/note_edit.html', context)
    elif request.method == 'GET':
        item = NoteItem.objects.get(id = note_id)
        item.subject = request.GET['note_subject']
        item.content = request.GET['note_content']
        item.save()
        return redirect('/login/')    

def search_process(request):
    if request.method == 'GET':
        keywords = request.GET['keywords']
        keywords = keywords.split()
        for i in range(0,len(keywords)):
            keywords[i] = keywords[i].lower()
        noteitems = []
        for item in NoteItem.objects.all():
            if item.owner.username == request.user.username:
                if(check_fixing(keywords,item)):
                    noteitems.append(item)
        context = {'username':request.user.username, 'noteitems':noteitems, 'total_notes':len(noteitems)}
        return render(request, './note_system/index.html', context)
    
def check_fixing(keywords, item):
    if len(keywords) == 0:
        return True
    tmp_s = item.subject+" "+item.content
    tmp_s = tmp_s.lower()
    for w in keywords:
        if w in tmp_s:
            return True
    return False