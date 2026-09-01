from django.contrib import admin
from apps.support.models import SupportCase, SupportMessage, KnowledgeBaseArticle

admin.site.register(SupportCase)
admin.site.register(SupportMessage)
admin.site.register(KnowledgeBaseArticle)
