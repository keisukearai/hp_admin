# -*- coding: utf-8 -*-
import unicodedata

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms

class Validate:
    """
    入力チェック用クラス
    """

    def validate_require(self, target, item):
        """
        必須チェック
        ----------
        Parameters
        ----------
        target: object
            入力値
        item: str
            項目名

        Returns
        -------
        ret: ValidationError
            処理結果
        """
        if target == None or len(target) == 0:
            return forms.ValidationError(u'%(item)sは必ず入力してください。',
                code='require', params={'item': item })
        return None

    def validate_max_byte(self, target, item, maxLength):
        """
        最大値(バイト数)チェック
        ----------
        Parameters
        ----------
        target: object
            入力値
        item: str
            項目名
        maxLength: int
            最大値

        Returns
        -------
        ret: ValidationError
            処理結果
        """
        if target == None:
            return None

        count =0
        for text in target:
            if unicodedata.east_asian_width(text) in 'FWA':
                count += 2
            else:
                count += 1

        if count > maxLength:
            return forms.ValidationError(u'%(item)sは%(maxLength)dバイト以内で入力してください。',
                code='invalidLength', params={'item': item, 'maxLength': maxLength})
        return None

    def validate_email(self, target, item=''):
        """
        必須チェック
        ----------
        Parameters
        ----------
        target: object
            入力値
        item: str
            項目名

        Returns
        -------
        ret: ValidationError
            処理結果
        """
        try:
            validate_email(target)
            return None
        except ValidationError:
            if item != '':
                item = f"{ item }は"
            return forms.ValidationError(u'%(item)sメールアドレスの形式で入力して下さい。',
                code='mail', params={'item': item })