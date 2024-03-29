# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class Company(models.Model):
    """
    会社モデル
    """
    name = models.CharField(verbose_name="会社名", max_length=10)
    zip = models.CharField(verbose_name="郵便番号", max_length=8)
    address = models.CharField(verbose_name="住所", max_length=256)
    tel = models.CharField(verbose_name="電話番号", max_length=15, blank=True, null=True)
    fax = models.CharField(verbose_name="FAX", max_length=15, blank=True, null=True)
    mail = models.EmailField(verbose_name="メールアドレス", blank=True, null=True)
    representative = models.CharField(verbose_name="代表者名", max_length=32)
    established = models.DateField(verbose_name="設立日")
    business_content = models.TextField(verbose_name="事業内容")
    capital = models.CharField(verbose_name="資本金", max_length=10)
    business_bank = models.TextField(verbose_name="取引銀行")
    accounting_period = models.CharField(verbose_name="決算期", max_length=10)
    corporate_number = models.CharField(verbose_name="法人番号", max_length=15, null=True)

    class Meta:
        db_table = 'company'
        verbose_name = f"{ db_table } (会社)"
        verbose_name_plural = f"{ db_table } (会社)"

    # 管理画面一覧表示時のタイトル
    def __str__(self):
        return f"{ self.name }"
class NewsCategory(models.Model):
    """
    ニュースカテゴリモデル
    """
    category_name = models.CharField(verbose_name="カテゴリ名", max_length=128)

    class Meta:
        db_table = 'newscategory'
        verbose_name = f"{ db_table } (ニュースカテゴリ)"
        verbose_name_plural = f"{ db_table } (ニュースカテゴリ)"

    def __str__(self):
        return self.category_name

class News(models.Model):
    """
    ニュースモデル
    """
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="タイトル", max_length=128)
    content = models.TextField(verbose_name="内容")
    entry_date = models.DateTimeField(verbose_name="登録日", default=timezone.now)
    disp_flag = models.BooleanField(verbose_name="表示フラグ", default=True)

    class Meta:
        db_table = 'news'
        verbose_name = f"{ db_table } (ニュース)"
        verbose_name_plural = f"{ db_table } (ニュース)"

    # 管理画面一覧表示時のタイトル
    def __str__(self):
        return f"【{ self.category }】{ self.title }"

class Inquiry(models.Model):
    """
    問合せモデル
    """
    title = models.CharField(verbose_name="タイトル", max_length=128)
    name = models.CharField(verbose_name="氏名", max_length=128)
    mail = models.EmailField(verbose_name="メールアドレス", blank=True, null=True)
    content = models.TextField(verbose_name="内容")
    confirm_flag = models.BooleanField(verbose_name="確認完了フラグ", default=False)
    entry_date = models.DateTimeField(verbose_name="登録日", default=timezone.now)

    class Meta:
        db_table = 'inquiry'
        verbose_name = f"{ db_table } (問合せ)"
        verbose_name_plural = f"{ db_table } (問合せ)"

    # 管理画面一覧表示時のタイトル
    def __str__(self):
        return f"【{ self.confirm_flag }】【タイトル】{ self.title }【登録日】{ self.entry_date.strftime('%Y/%m/%d %H:%M:%S') }"

class SiteLink(models.Model):
    """
    サイトリンクモデル
    """
    title = models.CharField(verbose_name="タイトル", max_length=256)
    url = models.URLField(verbose_name="サイトURL")
    content = models.TextField(verbose_name="内容", blank=True, null=True)
    disp_flag = models.BooleanField(verbose_name="表示フラグ", default=True)

    class Meta:
        db_table = 'sitelink'
        verbose_name = f"{ db_table } (サイトリンク)"
        verbose_name_plural = f"{ db_table } (サイトリンク)"

    # 管理画面一覧表示時のタイトル
    def __str__(self):
        return f"{ self.title }"