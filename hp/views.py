# -*- coding: utf-8 -*-
import logging
import json
import math

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
import db.db_connect as db

from hp.models import Company
from hp.models import NewsCategory
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
    ニュース一覧の取得
    """

    def get(self, request):
        # ログ出力
        logger = logging.getLogger('hp_admin')
        logger.debug(f"{ __class__.__name__ } get start")

        # limit
        limit = request.GET.get('limit', 5)
        logger.debug(f"limit:{ limit }")

        # ページ番号
        page = request.GET.get('page', 1)
        logger.debug(f"page:{ page }")

        # 検索ワード
        word = request.GET.get('word', '')

        # カテゴリ
        category = request.GET.get('category', '')

        # offsetの設定
        if int(page) == 1:
            offset = 0
        else:
            offset = limit * (int(page) - 1)

        # カテゴリ一覧の取得
        query_category = NewsCategory.objects.all()
        news_category = list(query_category.values())

        # 全カテゴリをリスト化する
        category_list = list(query_category.values_list('id', flat=True))

        # カテゴリの設定
        addWhere = ""
        if category != '':
            addWhere = f"and n.category_id = { category }"
            # リクエストパラメータを再設定
            category_list = [category]
        # print(category_list)

        # ニュース一覧の取得
        # query = News.objects.select_related().filter(disp_flag=True, title__contains=word, content__contains=word).order_by('-entry_date')[offset: offset + limit]
        # print(News.objects.select_related().all().query)
        # news = list(query.values('category', 'category_id'))
        sql = ("select "
                "n.id, n.title, n.content, n.entry_date, category_id, category_name "
                "from news n inner join newscategory c on n.category_id = c.id "
                "where n.disp_flag = '1' "
                f"and (n.title like '%{ word }%' or n.content like '%{ word }%') "
                f"{ addWhere } "
                "order by n.entry_date desc "
                f"limit { limit } offset { offset }")
        logger.debug(f"sql:{ sql }")
        news = db.execute(sql)

        # ニュース全件数の取得
        news_count = News.objects.filter(disp_flag=True, title__contains=word, content__contains=word, category_id__in=category_list).count()

        # トータルページの設定
        if int(news_count) == 0:
            total_pages = 0
        else:
            total_pages = math.ceil(news_count / limit)

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': 'ok',
            'news_count': news_count,
            'total_pages': total_pages,
            'news': news,
            'news_category': news_category
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
        # 取得できない場合
        if len(query) == 0:
            raise Http404("Question does not exist")

        newsdetail = list(query.values())

        query_category = NewsCategory.objects.filter(id=query[0].category_id)
        category = list(query_category.values())

        ##############################
        # 出力値の設定
        ##############################
        params = {
            'ret': 'ok',
            'newsdetail': newsdetail,
            'category': category
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
        # リクエストの取得
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

        ##############################
        # 入力チェック
        ##############################
        # 名前チェック
        # 必須
        chk = validate.validate_require(name, '名前')
        if chk != None:
            dic = {
                'msg': ''.join(chk),
                'msg_key': 'name'
            }
            messages.append(dic)
        else:
            # バイト長
            chk = validate.validate_max_byte(name, '名前', 128)
            if chk != None:
                dic = {
                    'msg': ''.join(chk),
                    'msg_key': 'name'
                }
                messages.append(dic)

        # メールチェック
        # 必須
        chk = validate.validate_require(mail, 'メール')
        if chk != None:
            dic = {
                'msg': ''.join(chk),
                'msg_key': 'mail'
            }
            messages.append(dic)
        else:
            chk = validate.validate_email(mail)
            if chk != None:
                dic = {
                    'msg': ''.join(chk),
                    'msg_key': 'mail'
                }
                messages.append(dic)

        # 表題チェック
        # 必須
        chk = validate.validate_require(title, '表題')
        if chk != None:
            dic = {
                'msg': ''.join(chk),
                'msg_key': 'title'
            }
            messages.append(dic)
        else:
            # バイト長
            chk = validate.validate_max_byte(title, '表題', 128)
            if chk != None:
                dic = {
                    'msg': ''.join(chk),
                    'msg_key': 'title'
                }
                messages.append(dic)

        # 内容チェック
        # 必須
        chk = validate.validate_require(content, '内容')
        if chk != None:
            dic = {
                'msg': ''.join(chk),
                'msg_key': 'content'
            }
            messages.append(dic)
        else:
            # バイト長
            chk = validate.validate_max_byte(content, '内容', 2048)
            if chk != None:
                dic = {
                    'msg': ''.join(chk),
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