from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError 
from Chat.models import Chat, Message

class RegisterView(TemplateView):
    template_name = "Chat/register.html"

    def dispatch(self, request, *args, **kwargs):
        
        context = {}
        
        if request.method == 'POST':
            usrname = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']        
            if password == password2:
                try:
                    User.objects.create_user(usrname, email, password)
                    login(request, authenticate(request,username=usrname,password=password))
                    return redirect("/chat")
                except IntegrityError:
                    context['error'] = "Такой пользователь уже существует"
                    return render(request, self.template_name,context)
            else:
                context['error']="Пароли не совпадают"
        return render(request, self.template_name,context)

class LoginView(TemplateView):
    template_name = "Chat/login.html"
    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect("/chat")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)

class MainPage(TemplateView):
    template_name="Chat/index.html"
    def get_chat_id(self,request,talker_user):
        current_user=request.user
        chat_qs=Chat.objects.filter(members=current_user).filter(members=talker_user)#.get().message_set.all()
        if not chat_qs:
            chat=Chat()
            chat.save()
            chat.members.add(current_user,talker_user)
            return chat.pk 
        
        else:
            return chat_qs.get().pk
    def dispatch(self,request):
        context={}
        if (request.method=='POST'):
            talker=request.POST['talker']
            try:
                talker_user=User.objects.get(username=talker)
            except User.DoesNotExist:
                context["error"]= "Пользователь не существует"
                return render(request,self.template_name,context)
            if talker_user==request.user:
                context["error"]="Нельзя начать диалог с самим собой"
                return render(request,self.template_name,context)
            if request.user.profile.banned:
                context["error"]="Вы забаннены"
                return render(request,self.template_name,context)
            if talker_user.profile.banned:
                context["error"]="Пользователь забаннен"
                return render(request,self.template_name,context)
            context['ready']=True
            context['talker']=request.POST['talker']
            context['curentuser']=request.user.username
            chat_id=self.get_chat_id(request,talker_user)
            context["chat"]=chat_id
        return render(request,self.template_name,context)


class StartChating(TemplateView):
    #template_name='Chat/room.html'
    template_name='Chat/room.html'
    def dispatch(self,request,room_name):
        chat=Chat.objects.get(pk=int(room_name))
        for i in chat.members.all():
            if request.user.username != i.username: talker=i.username
        mes=[]
        for i in chat.message_set.all():
            mes.append(i.messages)

        jmes='\n'.join(mes)
        jmes+='\n'
        context={'room_name':room_name,'old_mes':jmes,'talker':talker}
        return render(request,self.template_name,context)  

'''
def index(request):
    return render(request,'Chat/index.html')

Chat.objects.filter(members__in=[q,a]).distinct().get().message_set.all()
<QuerySet [<Message: qwerty: hi
aaaa: hello>, <Message: qwerty: how are u?>]>
'''


def logout_user(request):
    logout(request)
    return redirect('/chat')