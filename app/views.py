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
from calendar import monthrange

# Create your views here.
@login_required()
def home_screen_view(request):
    user = request.user
    context={}
    if user.is_authenticated:
        try:
            all_expenses = Expenses.objects.filter(owner = user)
            if all_expenses:
                if len(all_expenses)>6:
                    all_expenses = Expenses.objects.filter(owner = user).order_by('-id')[6]
                else:
                    all_expenses = Expenses.objects.filter(owner = user).order_by('-id')
        except:
            context['error']="no record found"
    return render(request,"")

def login_screen(request,**kwargs):
    user = request.user
    context={}
    if user.is_authenticated:
        return redirect("")
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email = email, password= password)
            if user:
                login(request,user)
                return redirect("")
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request,"",context)


def sign_up_screen(request,**kwargs):
    context={}
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid:
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = Account.objects.create_user(email = email ,username = username, password =password)
            if account:
                user = authenticate(email = email, password= password)
                if user:
                    login(request,user)
                    return redirect("")
    else:
        form = SignUpForm()
    context['sign_up_form'] = form
    return render(request,"",context)


@login_required
def logout_screen(request):
    logout(request)
    return redirect("")

def create_expenses(request):
    payload={}
    user =request.user
    if request.POST:
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        description =request.POST.get('description')
        dateUsage = request.POST.get('dateUsage')
        expenses_create = Expenses.objects.create(category = category, amount =amount, description= description, dateUsage = dateUsage)
        expenses_create.save()
        if expenses_create:
            expenses = Expenses.objects.filter(owner=user).order_by('-id')
            expenses_serializer = ExpensesSerializer()
            payload['created_expenses'] = expenses_serializer.serialize(expenses)[0]
    return HttpResponse(json.dumps(payload),content_type='application/json')

def update_expenses(request):
    payload={}
    user =request.user
    if request.POST:
        expenses_id= request.POST.get('expenses_id')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        description =request.POST.get('description')
        dateUsage = request.POST.get('dateUsage')
        try:
            expenses = Expenses.objects.get(id = expenses_id)
            if expenses:
                expenses_update = expenses.update(category = category, amount =amount, description= description, dateUsage = dateUsage)
                expenses_update.save()
            if expenses_update:
                expenses = Expenses.objects.get(id = expenses_id)
                expenses_serializer = ExpensesSerializer()
                payload['updated_expenses'] = expenses_serializer.serialize(expenses)
        except:
            payload['Error'] = "we couldn't find the data"
    return HttpResponse(json.dumps(payload),content_type='application/json')

def delete_expenses(request):
    payload={}
    user =request.user
    if request.POST:
        expenses_id= request.POST.get('expenses_id')
        try:
            expenses = Expenses.objects.get(id = expenses_id)
            if expenses:
                expenses_delete = expenses.delete()
                expenses_delete.save()
                payload['Response'] = "deleted"
        except:
            payload['Error'] = "we couldn't find the data"
    return HttpResponse(json.dumps(payload),content_type='application/json')

def get_monthly_expenses(request):
    payload={}
    payload['month_day']=[]
    user =request.user
    if request.POST:
        pickedyear = request.POST.get('picked_year')
        pickedmonth = request.POST.get('picked_month')
        payload['month_day']=[]
        days_in_month = monthrange(pickedyear,pickedmonth)[1]
        for i in range(days_in_month):
            payload["month_day"].append("{}/{}".format(pickedmonth,i+1))
        try:
            expenses = Expenses.objects.filter(owner = user)
            if expenses:
                try:
                    yearly_expense = expenses.objects.filter(pub_date__year=pickedyear)
                    if yearly_expense:
                        try:
                            monthly_expenses = yearly_expense.objects.filter(pub_date__month=pickedmonth)
                            if monthly_expenses:

                                """
                                to calculate the total sum of ecxpenses in a month
                                """
                                sum = 0
                                for expense in monthly_expenses:
                                    sum += expense.amount
                                expenses_serializer = ExpensesSerializer()

                                """
                                payload['all_expenses'] show every single expenses record in a month
                                """
                                payload['all_expenses'] = expenses_serializer.serialize(monthly_expenses)
                                payload['total sum'] = sum

                                """
                                calculate the total sum of expenses in a day in a month
                                
                                """
                                payload['month_day_expenses']=[]
                                for i in range(days_in_month):
                                    try:
                                        daily_expenses = monthly_expenses.objects.filter(pub_date__day=i+1)
                                        if daily_expenses:
                                            """
                                            add up the total amount of expenses in a day 
                                            """
                                            sum = 0
                                            for d_expense in daily_expenses:
                                                sum += d_expense.amount
                                            payload['month_day_expenses'].append(sum)
                                    except:
                                        """
                                        amount will be 0 if the queryset can't be found
                                        """
                                        payload['month_day_expenses'].append(0)
                                
                        except:
                            payload['monthly_expenses'] = "No record for month {}".format(pickedmonth)
                except:
                    payload['yearly_expenses'] = "No record for year {}".format(pickedyear)
        except:
            payload['Error'] = "no data"
    return HttpResponse(json.dumps(payload),content_type='application/json')


def monthly_expenses_datail_pagination(request):
    payload={}
    user = request.user
    if request.GET:
        pickedyear = request.GET.get('picked_year')
        pickedmonth = request.GET.get('picked_month')
        page_number = request.GET.get('page')
        try:
            user_expenses = Expenses.objects.filter(owner=user)
            if user_expenses:
                try:
                    yearly_expense = user_expenses.objects.filter(pub_date__year=pickedyear)
                    if yearly_expense:
                        try:
                            monthly_expenses = yearly_expense.objects.filter(pub_date__month=pickedmonth)
                            if monthly_expenses:
                                paginator = Paginator(monthly_expenses, 20) # Show 20 contacts per page.
                                payload['all_page_count']= paginator.num_pages
                                
                                expenses_serializer = ExpensesSerializer()
                                payload['p_monthly_expenses'] = expenses_serializer.serialize(paginator.get_page(page_number))
                        except:
                            payload['monthly_expenses'] = "No record for month {}".format(pickedmonth)
                except:
                    payload['yearly_expenses'] = "No record for year {}".format(pickedyear)
        except:
            payload['Error'] = "no data"     
        return HttpResponse(json.dumps(payload),content_type='application/json')