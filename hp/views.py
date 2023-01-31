# -*- coding: utf-8 -*-
import logging
import json

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from hp.models import Company
from hp.models import News
from hp.models import Inquiry
from hp.validate import Validate

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
        query = News.objects.filter(disp_flag=True).order_by('-entry_date')[:10]
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

class NewsDetailInfoView(TemplateView):
    """
    ニュース詳細の取得
    """

    def get(self, request, newsnumber):
        # ログ出力
        logger = logging.getLogger('hp_admin')
        logger.debug(f"{ __class__.__name__ } get start")
        logger.debug(f"newsnumber:{ newsnumber}")

        # ニュースの取得
        query = News.objects.filter(disp_flag=True, id=newsnumber)
        newsdetail = list(query.values())

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': 'ok',
            'newsdetail': newsdetail
        }

        logger.debug(f"{ __class__.__name__ } get end")
        return JsonResponse(params)

class InquiryEntryView(TemplateView):
    """
    問合せ登録
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request):
        # ログ出力
        logger = logging.getLogger('hp_admin')
        logger.debug(f"{ __class__.__name__ } post start")
        req = json.loads(request.body)

        # インスタンスの生成
        validate = Validate()

        # 氏名
        name = req.get('name', None)
        # メール
        mail = req.get('mail', None)
        # タイトル
        title = req.get('title', None)
        # 内容
        content = req.get('content', None)

        # 返却用メッセージ
        messages = []
        ret = 'ok'

        # 入力チェック
        # 名前チェック
        # 必須
        if name == None:
            dic = {
                'msg': '名前は必須です',
                'msg_key': 'name'
            }
            messages.append(dic)

        # メールチェック
        # 必須
        if mail == None:
            dic = {
                'msg': 'メールは必須です',
                'msg_key': 'mail'
            }
            messages.append(dic)
        else:
            chk = validate.validate_email(mail)
            if chk == False:
                dic = {
                'msg': 'メールアドレスのフォーマットが不正です。',
                'msg_key': 'mail'
                }
                messages.append(dic)

        # 表題チェック
        # 必須
        if title == None:
            dic = {
                'msg': '表題は必須です',
                'msg_key': 'title'
            }
            messages.append(dic)

        # 内容チェック
        # 必須
        if content == None:
            dic = {
                'msg': '内容は必須です',
                'msg_key': 'content'
            }
            messages.append(dic)

        # 入力チェックあり
        if len(messages) > 0:
            ret = 'ng'

        # 正常時
        else:
            # 問合せ登録
            inquiry = Inquiry(name=name, mail=mail, title=title, content=content)
            inquiry.save()

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': ret,
            'messages': messages
        }

        logger.debug(f"{ __class__.__name__ } post end")
        return JsonResponse(params)