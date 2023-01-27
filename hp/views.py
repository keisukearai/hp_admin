# -*- coding: utf-8 -*-
import logging
import json

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core import serializers

from hp.models import Company
from hp.models import News

class CompanyInfoView(TemplateView):
    """
    会社情報の取得
    """

    def get(self, request):
        # ログ出力
        logger = logging.getLogger('hp_admin')
        logger.debug(f"{ __class__.__name__ } get start")

        # 会社情報の取得
        query = Company.objects.all()
        company = list(query.values())

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': 'ok',
            'company': company
        }

        logger.debug(f"{ __class__.__name__ } get end")
        return JsonResponse(params)

class NewsInfoView(TemplateView):
    """
    ニュースの取得
    """

    def get(self, request):
        # ログ出力
        logger = logging.getLogger('hp_admin')
        logger.debug(f"{ __class__.__name__ } get start")

        # ニュースの取得
        query = News.objects.filter(disp_flag = True).order_by('-entry_date')[:3]
        news = list(query.values())

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': 'ok',
            'news': news
        }

        logger.debug(f"{ __class__.__name__ } get end")
        return JsonResponse(params)