from turtle import home
from django.urls import path
from app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",login_screen,name="login_screen"),
    path("sign_up/",sign_up_screen,name="sign_up_screen"),
    path("home/",home_screen,name='home_screen'),
    path('history/',history_screen,name='history_screen'),
    path("logout/",logout_screen,name="logout_screen"),
    path("profile/edit/<user_id>/",update_profile_screen,name="update_profile_screen"),
    path("create_expenses/",create_expenses, name='create_expenses'),
    path("update_expenses/",update_expenses,name="update_expenses"),
    path("delete_expenses/",delete_expenses,name='delete_expenses'),
    path("get_monthly_expenses_bar_chart/", get_monthly_expenses_bar_chart,name='get_monthly_expenses_bar_chart'),
    path('monthly_expenses_detail_pagination/',monthly_expenses_detail_pagination,name='monthly_expenses_detail_pagination'),
    path('get_recent_expenses/',get_recent_expenses,name='get_recent_expenses'),
    path('get_monthly_expenses_pie_chart/',get_monthly_expenses_pie_chart,name='get_monthly_expenses_pie_chart'),
    path('get_expenses_detail/',get_expenses_detail,name='get_expenses_detail'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_comfirm.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
]
