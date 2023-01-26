# -*- coding: utf-8 -*-
from django.urls import path
import hp.views as views

# アプリケーション名
app_name = 'hp'

# URL
urlpatterns = [
    # 会社情報の取得
    path('company', views.CompanyInfoView.as_view(), name='company'),
]