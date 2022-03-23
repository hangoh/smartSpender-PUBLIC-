from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.paginator import Paginator
from app.forms import *
from app.models import Expenses
from app.utils import *
import calendar

# Create your views here.
@login_required(login_url="login_screen")
def home_screen(request,*args, **kwargs):
    user = request.user
    expenses_category= ['grocery','rent and fees','transport','food and drinks','entertainment','medical and healthcare','others']
    context={}
    context['user'] = user
    context['expenses_category'] = expenses_category
    return render(request,"home.html",context)

@login_required(login_url="login_screen")
def history_screen(request,*args, **kwargs):
    user = request.user
    expenses_category= ['grocery','rent and fees','transport','food and drinks','entertainment','medical and healthcare','others']
    context={}
    context['user'] = user
    context['expenses_category'] = expenses_category
    return render(request,"history.html",context)

def login_screen(request,**kwargs):
    user = request.user
    context={}
    if user.is_authenticated:
        return redirect("home_screen")
    if request.POST:
        forms = LoginForm(request.POST)
        if forms.is_valid:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email = email, password= password)
            if user:
                login(request,user)
                return redirect("home_screen")
        else:
            forms = LoginForm()
    else:
        forms = LoginForm()
    
    context['forms'] = forms
    return render(request,"login_in.html",context)


def sign_up_screen(request,*args, **kwargs):
    context={}
    if request.POST:
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data.get('email')
            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password1')
            currency = forms.cleaned_data.get('currency')
            user = Account.objects.create_user(email = email, username = username, password = password,currency=currency)
            if user:
                auth_user = authenticate(email=email, password=password)
                if auth_user:
                    login(request,auth_user)
                    return redirect('home_screen')
        else:
            context['errors'] =forms
    else:
        forms = RegisterForm()
    context['register_form'] = forms
    return render (request,'sign_up.html',context)

@login_required(login_url="login_screen")
def update_profile_screen(request,*args, **kwargs):
    user_id =kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)
    context={}
    context['user'] = account
    if account==request.user:
        if request.POST:
            forms = UpdateDetailForm(request.POST,instance=account)
            if forms.is_valid():
                account.username = request.POST.get('username')
                account.email = request.POST.get('email')
                account.save()
                return redirect('home_screen')
            else:
                context['form'] =forms
        else:
            forms = UpdateDetailForm()
            context['form'] =forms
    
    return render(request,'edit_profile.html',context)


@login_required(login_url="login_screen")
def logout_screen(request,*args, **kwargs):
    logout(request)
    return redirect("login_screen")

@login_required(login_url="login_screen")
def create_expenses(request,*args, **kwargs):
    payload={}
    user =request.user
  
    if request.POST:
        title = request.POST.get('title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        description =request.POST.get('description')
        dateUsage = request.POST.get('dateUsage')
        try:
            expenses_create = Expenses.objects.create(owner=user,title = title,category = category, amount =amount, description= description, dateUsage = dateUsage)
            expenses_create.save()
            payload['Response'] = 'created'
            expenses_create = Expenses.objects.filter(owner=user,title = title,category = category, amount =amount, description= description, dateUsage = dateUsage)
            expenses_serializer = ExpensesSerializer()
            payload['expenses_create'] = expenses_serializer.serialize(expenses_create)[0]
        except ZeroDivisionError as e:
            payload['error'] = e
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.pk}
    return HttpResponse(json.dumps(payload),content_type='application/json')


@login_required(login_url="login_screen")
def update_expenses(request,*args, **kwargs):
    payload={}
    user =request.user
    if request.POST:
        expenses_id= request.POST.get('expenses_id')
        title = request.POST.get('title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        description =request.POST.get('description')
        dateUsage = request.POST.get('dateUsage')
        try:
            
            expenses_update = Expenses.objects.get(id = expenses_id)
            
            if expenses_update:
                expenses_update.title = title
                expenses_update.category = category
                expenses_update.amount = amount
                expenses_update.dateUsage = dateUsage
                expenses_update.description =description
                expenses_update.save()
                expenses = Expenses.objects.filter(id = expenses_id)
                expenses_serializer = ExpensesSerializer()
                payload['updated_expenses'] = expenses_serializer.serialize(expenses)[0]
                payload['response'] = 'updated'
        except ZeroDivisionError as e:
            print(e)
            payload['error'] = "we couldn't find the data"
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.pk}
    return HttpResponse(json.dumps(payload),content_type='application/json')


@login_required(login_url="login_screen")
def delete_expenses(request,*args, **kwargs):
    payload={}
    user =request.user
    if request.GET:
        expenses_id= request.GET.get('expenses_id')
        try:
            expenses = Expenses.objects.get(id = expenses_id)
            print(expenses)
            if expenses:
                expenses_delete = expenses.delete()
                payload['Response'] = "deleted"
            else:
                payload['Error'] = "we couldn't find the data"
        except ZeroDivisionError as e:
            print(e)            
    return HttpResponse(json.dumps(payload),content_type='application/json')


@login_required(login_url="login_screen")
def get_monthly_expenses_bar_chart(request,*args, **kwargs):
    payload={}
    user =request.user
    if request.GET:
        pickedyear = int(request.GET.get('picked_year'))
        pickedmonth = int(request.GET.get('picked_month'))
        payload['month_day_label']=[]
        days_in_month = calendar.monthrange(pickedyear,pickedmonth)[1]
        for i in range(days_in_month):
            payload["month_day_label"].append("{}/{}".format(pickedmonth,i+1))
        try:
            expenses = Expenses.objects.filter(owner = user,dateUsage__year=pickedyear,dateUsage__month=pickedmonth)
            if expenses:
                """
                to calculate the total sum of expenses in a month
                """
                sum = 0
                for expense in expenses:
                    sum += expense.amount
                expenses_serializer = ExpensesSerializer()
                """
                payload['all_expenses'] show every single expenses record in a month
                """
                payload['all_expenses'] = expenses_serializer.serialize(expenses)
                
                payload['total_sum'] = "{}".format(sum)
                """
                calculate the total sum of expenses in a day of a month
                
                """
                
                payload['month_day_expenses']=[]
                for i in range(days_in_month):
                    try:
                        daily_expenses = Expenses.objects.filter(owner=user,dateUsage__year=pickedyear,dateUsage__month=pickedmonth,dateUsage__day=i+1)
                        if daily_expenses:
                            """
                            add up the total amount of expenses in a day 
                            """
                            sum = 0
                            for d_expense in daily_expenses:
                                sum += d_expense.amount
                            payload['month_day_expenses'].append("{}".format(sum))
                        else:
                            payload['month_day_expenses'].append(0) 
                    except ZeroDivisionError as e:
                        """
                        amount will be 0 if the queryset can't be found
                        """
                        print(e)
            else:
                payload['total_sum'] = 0
                                           
        except :
            payload['total_sum'] = 0
            payload['No_expenses'] = True  
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.pk} 
    return HttpResponse(json.dumps(payload),content_type='application/json')

@login_required(login_url="login_screen")
def monthly_expenses_detail_pagination(request,*args, **kwargs):
    payload={}
    user = request.user
    if request.GET:
        pickedyear = request.GET.get('picked_year')
        pickedmonth = request.GET.get('picked_month')
        page_number = int(request.GET.get('page'))
        
        try:
            user_expenses = Expenses.objects.filter(owner = user,dateUsage__year=pickedyear,dateUsage__month=pickedmonth).order_by('dateUsage')
            if user_expenses:
                paginator = Paginator(user_expenses, 8) # Show 20 expenses per page.
                if(page_number <= paginator.num_pages):
                    payload['all_page_count']= paginator.num_pages
                    payload['current_page']= page_number
                    expenses_serializer = ExpensesSerializer()
                    payload['p_monthly_expenses'] = expenses_serializer.serialize(paginator.get_page(page_number))
                    payload['Response'] = 'get'
                       
        except:
            payload['Error'] = "no data" 
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.pk}         
    return HttpResponse(json.dumps(payload),content_type='application/json')


@login_required(login_url="login_screen")
def get_recent_expenses(request,*args, **kwargs):
    user = request.user
    payload={}
    if user.is_authenticated:
        try:
            all_expenses = Expenses.objects.filter(owner = user)
            if all_expenses:
                if len(all_expenses)>10:
                    all_expenses = Expenses.objects.filter(owner = user).order_by('-id')[:10]
                else:
                    all_expenses = Expenses.objects.filter(owner = user).order_by('-id')
                expenses_serializer = ExpensesSerializer()
                payload['recent_expenses'] = expenses_serializer.serialize(all_expenses)
                payload['Response'] = 'data_found'
            else:
                payload['Response'] = 'no_data_found'
        except ZeroDivisionError as e:
            print(e)
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.pk}
    return HttpResponse(json.dumps(payload),content_type='application/json')


@login_required(login_url="login_screen")
def get_monthly_expenses_pie_chart(request,*args, **kwargs):
    payload={}
    expenses_category= ['grocery','rent and fees','transport','food and drinks','entertainment','medical and healthcare','others']
    payload["category_label"] = []
    payload["category_sum"] = []
    total_sum = 0
    user =request.user
    if request.GET:
        pickedyear = request.GET.get('picked_year')
        pickedmonth = request.GET.get('picked_month')
        for e_x in expenses_category:
            try:
                expenses = Expenses.objects.filter(owner = user,dateUsage__year=pickedyear,dateUsage__month=pickedmonth,category=e_x)
                if expenses:
                    total_expenses = 0
                    for ex in expenses:
                        total_expenses+=ex.amount
                        total_sum +=ex.amount
                    payload["category_label"].append(e_x)
                    payload["category_sum"].append('{}'.format(total_expenses))
            except ZeroDivisionError as e:
                print(e)
    payload['total_sum'] ="{}".format(total_sum)
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.pk}
    return HttpResponse(json.dumps(payload),content_type='application/json')

@login_required(login_url="login_screen")
def get_expenses_detail(request,*args, **kwargs):
    payload={}
    user = request.user
    if request.GET:
        expenses_id = request.GET.get('id')
        try:
            user_expenses = Expenses.objects.filter(owner = user,id=expenses_id)
            if user_expenses:
                expenses_serializer = ExpensesSerializer()
                payload['user_expenses'] = expenses_serializer.serialize(user_expenses)[0]
                payload['Response']='get'
        except:
            payload['error'] = "no data" 
    payload['user']={'email':user.email, 'username':user.username,'currency':user.currency,'id':user.id}         
    return HttpResponse(json.dumps(payload),content_type='application/json')