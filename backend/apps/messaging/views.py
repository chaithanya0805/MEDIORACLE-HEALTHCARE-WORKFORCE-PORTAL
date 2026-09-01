from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.messaging.models import Conversation, Message
from apps.messaging.serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        message_text = request.data.get('message')
        recipient_id = request.data.get('recipient')
        
        if not message_text:
            return Response({"success": False, "message": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(
            sender=request.user,
            recipient_id=recipient_id,
            conversation=conversation,
            message=message_text
        )

        return Response({
            "success": True,
            "message": "Message sent successfully",
            "data": MessageSerializer(msg).data
        })
