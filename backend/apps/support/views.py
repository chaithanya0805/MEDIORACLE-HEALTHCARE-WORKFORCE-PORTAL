from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid
from apps.accounts.models import Role
from apps.support.models import SupportCase, SupportMessage, KnowledgeBaseArticle, CaseStatus
from apps.support.serializers import SupportCaseSerializer, SupportMessageSerializer, KnowledgeBaseArticleSerializer

class SupportCaseViewSet(viewsets.ModelViewSet):
    queryset = SupportCase.objects.all()
    serializer_class = SupportCaseSerializer
    filterset_fields = ['status', 'priority', 'category']

    def get_queryset(self):
        user = self.request.user
        if user.role in [Role.SUPER_ADMIN, Role.SUPPORT_AGENT]:
            return SupportCase.objects.all()
        return SupportCase.objects.filter(user=user)

    def perform_create(self, serializer):
        c_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        serializer.save(user=self.request.user, case_id=c_id)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        case = self.get_object()
        msg_text = request.data.get('message')
        if not msg_text:
            return Response({"success": False, "message": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        msg = SupportMessage.objects.create(
            support_case=case,
            sender=request.user,
            message=msg_text
        )

        if request.user.role in [Role.SUPER_ADMIN, Role.SUPPORT_AGENT] and case.status == CaseStatus.OPEN:
            case.status = CaseStatus.IN_PROGRESS
            case.assigned_agent = request.user
            case.save()

        return Response({
            "success": True,
            "message": "Reply posted successfully",
            "data": SupportMessageSerializer(msg).data
        })

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        case = self.get_object()
        resolution = request.data.get('resolution', '')
        
        case.status = CaseStatus.RESOLVED
        case.resolution = resolution
        case.save()

        return Response({
            "success": True,
            "message": "Support case resolved successfully",
            "data": SupportCaseSerializer(case).data
        })

class KnowledgeBaseArticleViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBaseArticle.objects.all()
    serializer_class = KnowledgeBaseArticleSerializer
    filterset_fields = ['category']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
