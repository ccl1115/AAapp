# -*- coding: utf8 -*-
from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import simplejson

from AAapp import settings

from AA.models import AccountInfo, Expense, Approve
from AA.forms import NewExpenseForm, NewAccountForm, LoginForm

def welcome(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return render_to_response('admin.html', 
                    { 'allusers':User.objects.filter(is_staff=False) },
                    context_instance=RequestContext(request))
        return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
            loginForm = LoginForm(request.POST)
            if loginForm.is_valid():
                cleaned_data = loginForm.clean()
                user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('/')
                else:
                    loginForm.errors['error: '] = 'wrong username or password'
                    return render_to_response('login.html', { 'form' : loginForm },
                            context_instance=RequestContext(request))
                    
        else:
            loginForm = LoginForm()
        return render_to_response('login.html', { 'form' : loginForm },
                context_instance=RequestContext(request))


@login_required
def new_expense(request):
    ''''''
    if not request.user.is_superuser:
        return render_to_response('error.html', 
                { 'error': 'Permission Denied.' })
    if request.method == 'POST':
        expense = Expense()
        newExpenseForm = NewExpenseForm(request.POST)
        if newExpenseForm.is_valid():
            cd = newExpenseForm.cleaned_data
            expense.title = cd['title']
            expense.money = cd['money']
            expense.save()
            expense.participants = cd['participants']
            expense.save()
            each = expense.each()
            for user in expense.participants.all():
                try:
                    user.accountinfo.balence -= each
                    user.accountinfo.save()
                except Exception as e:
                    print e
                    pass
            subject = 'AAapp - ' + expense.title
            send_mail(subject, '你花费了 %d 于 %s' % (each, expense.pub_datetime),
                    settings.SEND_MAIL_USER,
                    [user.email for user in expense.participants.all()],
                    fail_silently=False)
            return redirect('/')
    else:
        newExpenseForm = NewExpenseForm()
    return render_to_response('new_expense.html', { 'form' : newExpenseForm },
            context_instance=RequestContext(request))

@login_required
def view_expense(request, id):
    ''''''
    try:
        expense = Expense.objects.get(id=int(id))
        if not request.user in expense.participants.all():
            return render_to_response('error.html',
                    { 'error' : 'Permission Denied' })
        return render_to_response('view_expense.html', { 'expense' : expense },
                context_instance=RequestContext(request))
    except Exception as e:
        print unicode(e)
        raise Http404

@login_required
def new_account(request):
    if not request.user.is_superuser:
        return render_to_response('error.html', { 'error' : 'Permission Denied' })
    if request.method == 'POST':
        newAccountForm = NewAccountForm(request.POST) 
        if newAccountForm.is_valid():
            cd = newAccountForm.clean()
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.accountinfo = AccountInfo()
            user.accountinfo.balence = 0.0
            user.accountinfo.save()
            user.save()
            return redirect('/')
    else:
        newAccountForm = NewAccountForm()
    return render_to_response('new_account.html', { 'form' : newAccountForm })


@login_required
def edit_account(request):
    pass


@login_required
def signoff(request):
    ''''''
    if request.user.is_authenticated():
        logout(request)
        return redirect('/')

@login_required
def ajax_balence_detail(request, id):
    try:
        user = User.objects.get(id=int(id))
        return simplejson.dumps(user.expense_set)
    except Exception as e:
        print e
        raise Http404
