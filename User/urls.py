#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：urls.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:24 
"""
from django.urls import path, include, re_path
from User.Views.AccountConfirmEmail import AccountConfirmEmail
from User.Views.Frontend.LoginLogsAPIs import LoginLogsList
from User.Views.Login import Login


urlpatterns = [
    re_path('frontend/rest-auth/login/', Login.as_view(), name='rest_login'),
    path('frontend/rest-auth/', include('rest_auth.urls')),

    path('frontend/rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^frontend/rest-auth/user-confirm-email/(?P<key>[-:\w]+)/$', AccountConfirmEmail, name='account_confirm_email'),
    re_path(r'^frontend/rest-auth/user-confirm-email/', AccountConfirmEmail, name='account_email_verification_sent'),

    path('frontend/login-logs-list/', LoginLogsList.as_view(), name='login-logs-list'),
]