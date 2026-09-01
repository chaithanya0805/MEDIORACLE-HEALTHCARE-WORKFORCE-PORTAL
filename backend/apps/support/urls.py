from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.support.views import SupportCaseViewSet, KnowledgeBaseArticleViewSet

router = DefaultRouter()
router.register('cases', SupportCaseViewSet, basename='support-case')
router.register('articles', KnowledgeBaseArticleViewSet, basename='kb-article')

urlpatterns = [
    path('', include(router.urls)),
]
