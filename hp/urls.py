# -*- coding: utf-8 -*-
from django.urls import path
import hp.views as views

# アプリケーション名
app_name = 'hp'

# URL
urlpatterns = [
    # 会社情報の取得
    path('company', views.CompanyInfoView.as_view(), name='company'),
    # Newsの取得
    path('news', views.NewsInfoView.as_view(), name='news'),
    # News詳細の取得
    path('news/<int:newsnumber>/', views.NewsDetailInfoView.as_view(), name='newsdetail'),
    # 問合せ登録
    path('inquiry', views.InquiryEntryView.as_view(), name='inquiry'),
    # 未確認の問合せ件数
    path('inquiry_count', views.InquiryCountView.as_view(), name='inquiry_count'),
    # サイトリンクの取得
    path('sitelink', views.SiteLinkView.as_view(), name='sitelink'),
]