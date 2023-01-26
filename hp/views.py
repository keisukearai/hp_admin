# -*- coding: utf-8 -*-
import logging
import json

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.core import serializers

from hp.models import Company

class CompanyInfoView(TemplateView):
    """
    会社情報の取得
    """

    def get(self, request):
        # ログ出力
        logger = logging.getLogger('hp_admin')
        logger.debug(f"{ __class__.__name__ } get start")

        # 会社情報の取得
        company = list(Company.objects.all().values())

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': 'ok',
            'company': company
        }

        logger.debug(f"{ __class__.__name__ } get end")
        return JsonResponse(params)