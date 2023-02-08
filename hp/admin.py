# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from hp.models import Company
from hp.models import NewsCategory
from hp.models import News
from hp.models import Inquiry

admin.site.register(Company)
admin.site.register(NewsCategory)
admin.site.register(News)
admin.site.register(Inquiry)