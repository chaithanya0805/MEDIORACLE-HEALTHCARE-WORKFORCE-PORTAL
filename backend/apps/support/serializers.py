from rest_framework import serializers
from apps.support.models import SupportCase, SupportMessage, KnowledgeBaseArticle

class SupportMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = SupportMessage
        fields = '__all__'

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

class SupportCaseSerializer(serializers.ModelSerializer):
    messages = SupportMessageSerializer(many=True, read_only=True)
    user_name = serializers.SerializerMethodField()
    assigned_agent_name = serializers.SerializerMethodField()

    class Meta:
        model = SupportCase
        fields = '__all__'
        read_only_fields = ['case_id', 'user', 'assigned_agent', 'resolution', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_assigned_agent_name(self, obj):
        if obj.assigned_agent:
            return f"{obj.assigned_agent.first_name} {obj.assigned_agent.last_name}"
        return None

class KnowledgeBaseArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBaseArticle
        fields = '__all__'
