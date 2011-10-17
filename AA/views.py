# -*- coding: utf8 -*-
from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth import authenticate, login, logout

from AA.models import AccountInfo, Expense, Approve
from AA.forms import NewExpenseForm, NewAccountForm, LoginForm

def welcome(request):
    if request.user.is_authenticated():
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
    if request.method == 'POST':
        expense = Expense()
        expense.host = request.user
        newExpenseForm = NewExpenseForm(request.POST, instance=expense)
        if newExpenseForm.is_valid():
            newExpense = newExpenseForm.save()
            approve = Approve()
            approve.expense = newExpense
            approve.status = 'I'
            approve.save()
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
        return render_to_response('view_expense.html', { 'expense' : expense },
                context_instance=RequestContext(request))
    except Exception as e:
        print unicode(e)
        raise Http404

@login_required
def new_account(request):
    pass

@login_required
def edit_account(request):
    pass


@login_required
def signoff(request):
    ''''''
    if request.user.is_authenticated():
        logout(request)
        return redirect('/')

def help(request):
    return render_to_response('help.html')
