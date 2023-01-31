# -*- coding: utf-8 -*-

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class Validate:

    def validate_email(self, mail):
        try:
            validate_email(mail)
            return True
        except ValidationError:
            return False
